from flask import jsonify, request, url_for, abort, current_app
from application import db
from application.models import User, Message, Post, Store, Experiment, save_image
from application.api import bp
from application.api.auth import token_auth
from application.api.errors import bad_request

from datetime import datetime
import uuid


@bp.route('/users/current', methods=['GET'])
@token_auth.login_required
def get_current_user():
    current_user = token_auth.current_user()
    return jsonify(current_user.to_dict())


@bp.route('/users/all', methods=['GET'])
@token_auth.login_required
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = User.to_collection_dict(User.query, page, per_page, 'api.get_users')
    return jsonify(data)


@bp.route('/users/<int:id>', methods=['GET'])
@token_auth.login_required
def get_user(id):
    return jsonify(User.query.get_or_404(id).to_dict())


@bp.route('/users/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_user(id):
    if token_auth.current_user().id != id:
        abort(403)
    user = User.query.get_or_404(id)
    data = request.get_json() or {}
    if 'username' in data and data['username'] != user.username and \
            User.query.filter_by(username=data['username']).first():
        return bad_request('please use a different username')
    user.from_dict(data, new_user=False)
    db.session.commit()
    return jsonify(user.to_dict())

@bp.route('/users/followers/<int:id>', methods=['GET'])
@token_auth.login_required
def get_followers(id):
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = User.to_collection_dict(user.followers, page, per_page, 'api.get_followers', id=id)
    return jsonify(data)


@bp.route('/users/followed/<int:id>', methods=['GET'])
@token_auth.login_required
def get_followed(id):
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = User.to_collection_dict(user.followed, page, per_page, 'api.get_followed', id=id)
    return jsonify(data)


@bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json() or {}
    if 'username' not in data or 'password' not in data:
        return bad_request('must include username and password fields:' + str(data))
    if User.query.filter_by(username=data['username']).first():
        return bad_request('please use a different username')
    user = User()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_user', id=user.id)
    return response



@bp.route('/messages/all', methods=['GET'])
@token_auth.login_required
def all_the_messages():
    current_user = token_auth.current_user()
    current_user.last_message_read_time = datetime.utcnow()
    # current_user.add_notification('unread_message_count', 0)
    db.session.commit()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    messages = current_user.messages_received.order_by(Message.timestamp.desc())
    data = Message.to_collection_dict(messages, page, per_page, 'api.all_the_messages')
    return jsonify(data)


@bp.route('/messages/empty', methods=['GET'])
@token_auth.login_required
def delete_all_the_messages():
    user = User.query.filter_by(username='charliebot').first_or_404()
    current_user = token_auth.current_user()
    if user == current_user:    
        current_user.last_message_read_time = datetime.utcnow()
        current_user.add_notification('unread_message_count', 0)
        db.session.commit()
        messages = current_user.messages_received.order_by(Message.timestamp.desc())
        if messages:
            for m in messages:
                db.session.delete(m)
            db.session.commit()
        data = {'result': 'queue is empty'}
    else:
        data = {'result': 'invalid request'}
    return jsonify(data)


@bp.route('/messages/<int:id>', methods=['GET'])
@token_auth.login_required
def get_message(id):
    message = Message.query.get_or_404(id)
    current_user = token_auth.current_user()
    if message.sender_id == current_user.id:
        return jsonify(message.to_dict())
    elif message.recipient_id == current_user.id:
        return jsonify(message.to_dict())
    else:
        return bad_request("current user can not request this message")
    

@bp.route('/posts', methods=['POST'])
@token_auth.login_required
def publish():
    current_user = token_auth.current_user()
    data = request.get_json() or {}
    try:
        content = data['content']
    except KeyError:
        content = '\n'.join([f'{str(k):s}: {str(v)}' for k, v in data.items()])
    new_post = Post(content=content, author=current_user)
    db.session.add(new_post)
    db.session.commit()
    return jsonify(current_user.to_dict())


@bp.route('/experiment', methods=['POST'])
@token_auth.login_required
def upload_experiment():
    current_user = token_auth.current_user()
    current_app.logger.info(f"request {request != None}")
    _title = '1'
    _body = '1'
    _sender_id = '1'
    error = False
    try:
        data = request.get_json() or {}
        current_app.logger.info(str(data))
    except Exception as message:
        current_app.logger.error(str(message))
        error = True
    try:
        current_app.logger.info(str(data))
        _title = data.get('title') or '2'
        _body = data.get('body') or '2'
        _sender_id = data.get('sender_id') or '2'
        current_app.logger.info(_title)
        current_app.logger.info(_body)
        current_app.logger.info(_sender_id)        
    except Exception as message:
        current_app.logger.error(str(message))
        error = True
    if error:
        result = {'title': _title, 'body': _body, 'sender_id': sender_id}
        current_app.logger.error(result)
        return jsonify(result)
    else:
        current_app.logger.info("new_experiment start")
        _resource_uuid = uuid.uuid4().hex
        store = Store.create(current_user)        
        new_experiment = Experiment(resource_uuid=_resource_uuid,
                                    user_id=_sender_id,
                                    title=_title,
                                    body=_body,
                                    store_id=store.id)
        db.session.add(new_experiment)
        db.session.commit()
        current_app.logger.info("new_experiment done")
        return jsonify(new_experiment.to_dict())


@bp.route('/experiment/picture/<string:resource_uuid>', methods=['POST'])
@token_auth.login_required
def upload_experiment_picture(resource_uuid):
    current_app.logger.info(f"/experiment/picture/{resource_uuid:s} start")
    current_user = token_auth.current_user()
    current_app.logger.info(f"request {request != None}")
    error = False
    reason = 0
    try:
        image = request.files['image']
        current_app.logger.info("got image file")
    except Exception as message:
        current_app.logger.error(str(message))
        error = True
        reason = 1
    if image == None:
        current_app.logger.error('image == None')
        error = True
        reason = 2
    else:
        current_app.logger.info("image != None")
        resource = Experiment.query.filter_by(resource_uuid=resource_uuid).first_or_404()
        current_app.logger.info(f"got resource {resource_uuid:s} - {resource.id:d}")        
        store = Store.query.filter_by(id=resource.store_id).first_or_404()
        current_app.logger.info(f"got store {store.id:d}")        
        try:
            save_image(image, store)
            current_app.logger.info(f"save image")                    
        except Exception as message:
            current_app.logger.error(str(message))
            error = True
            reason = 3
    current_app.logger.info(f"done")                    
    result = {'error': error, 'reason': reason}
    current_app.logger.info(f"/experiment/picture/{resource_uuid:s} done")
    return jsonify(result)

