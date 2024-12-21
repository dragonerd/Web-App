from flask import flash, redirect, url_for, Blueprint
from dbconfig import db
from models.models import confirm_token
from models.models import UserInfo


user_activate = Blueprint('user_activate', __name__)

@user_activate.route('/confirmar/<token>', methods=['GET'])
def confirm_email(token):
    email = confirm_token(token)
    if email:
        user = db.session.query(UserInfo).filter_by(email=email).first()
        if user:
            username = user.username
            status = user.status
            email = user.email
            user.status = True
            user.trysend = 0
            db.session.commit()
        flash('Tu cuenta ha sido confirmada. ¡Bienvenido!', 'success')
        print(f'[SUCCESS][ACTIVATE][GET] = {username} - {email} - {user.status}')
        return redirect(url_for('user_login.login'))
    else:
        flash('El enlace de confirmación es inválido o ha expirado.', 'danger')
        return redirect(url_for('user_login.login'))