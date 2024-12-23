from options import time
from flask import request, render_template, Blueprint, session, flash, redirect, url_for
from dbconfig import argon2, db, app
from security import max_attempts
from text import text_data
from models.models import send_confirmation_email, UserInfo
from models.login import LoginForm, validate_csrf_and_form
from tokenauth import generate_jwt
from routes.csrf import csrf_check_status


user_login = Blueprint('user_login', __name__)

@user_login.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    app.logger.info('\033[1;32m[LOGIN][PRE-CHECK]\033[0m %s', str(csrf_check_status()))
    if request.method == 'POST':
        if validate_csrf_and_form(form):
            username = form.username.data
            password = form.password.data
            user = db.session.query(UserInfo).filter_by(username=username).first()
            app.logger.info(f'\033[1;32m[VALIDATING...] {user.username} {form.csrf_token.data}\033[0m')
        if user:
            app.logger.info('\033[1;32m[LOGIN][LOADING...]\033[0m %s', str(csrf_check_status()))
            if user.trysend > max_attempts:
                app.logger.info(f'\033[1;32m[LOGIN][ERROR][POST] Status:{user.status} | Send Email Status: BLOCKED | {username} | {time()}\033[0m')
                flash(f'Muchos intentos activando cuenta, intentalo mas tarde', 'error')
                return redirect(url_for('index'))
            if not user.status:
                db.session.commit()
                if app.config['SEND_EMAIL_REGISTER']:
                    send_confirmation_email(user.email)
                    user.trysend +=1
                    app.logger.info(f'\033[1;32m[LOGIN][ERROR][POST] Status:{user.status} | Send Email Status: {user.trysend} | {username} | {time()}\033[0m')
                    flash('Tu cuenta no ha sido activada, se te ha reenviado un correo de confirmacion', 'warning')
                    return redirect(url_for('index'))
            app.logger.info(f'\033[91m[LOGIN][WARINING][POST] Status:{user.status} | Send Email Status: {user.trysend} | {username} | {time()}\033[0m')
        if user and argon2.check_password_hash(user.password, password) or user.temp_password == password:
            jwt_token = generate_jwt(user.id_profile)
            session['jwt_token'] = jwt_token
            app.logger.info(f'\033[1;32m[LOGIN][SUCCESS][POST] {username} -  {time()}\033[0m')
            flash(f'Bienvenido! {username}', 'success')
            app.logger.info('\033[1;32m[LOGIN][SUCCESS][POST]\033[0m %s', str(csrf_check_status()))
            return redirect(url_for('user_dashboard.dashboard'))
        
        else:
            app.logger.info(f'\033[1;32m[LOGIN][ERROR][POST]{username} - {password}\033[0m')
            flash('Los datos ingresados son incorrectos', 'error')
            return render_template('login/login.html', text_data=text_data, form=form)
    return render_template('login/login.html', text_data=text_data, form=form)