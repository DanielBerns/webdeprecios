from flask import render_template

def get_reset_password_messages(user):
    token = user.get_reset_password_token()
    text_message = render_template('auth/reset_password_message.txt', 
                                user=user, 
                                token=token)
    html_message = render_template('auth/reset_password_message.html', 
                                user=user, 
                                token=token)
    return text_message, html_message
