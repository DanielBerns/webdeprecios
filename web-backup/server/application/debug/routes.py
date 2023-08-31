from application.debug import bp
from flask import render_template, current_app

@bp.route('/show/<string:state>', methods=['GET'])
def show(state):
    return render_template('debug/show.html', 
                           state=state, 
                           html_title='debug-show',
                           website=current_app.config['WEBSITE'])
