from application import create_app, db
from application.models import User, Publisher, Admin, Store, Post

app = create_app()

@app.context_processor
def utility_processor():
    def format_user_rights(value):
        return f'{bin(value)[2:]}'
    
    def website():
        return f"{app.config['WEBSITE']}"
    
    return { 'format_user_rights': format_user_rights,
             'website': website}


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Publisher': Publisher, 'Admin': Admin, 'Store': Store, 'Post': Post}
