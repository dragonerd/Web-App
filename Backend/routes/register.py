from flask import flash, redirect, url_for, render_template, Blueprint, request
from dbconfig import argon2, db, app
from models.register import pass_generator
from models.register import RegisterForm
from models.models import send_confirmation_email, UserInfo
from text import text_data
import re


user_register = Blueprint('user_register', __name__)

#Register Version 1.0.0 DONE
@user_register.route('/new', methods=['GET', 'POST'])
def newregister():
    form = RegisterForm()
    if request.method == "POST":
        if form.validate_on_submit():
            fname = form.fname.data
            lname = form.lname.data
            username_escaped = re.escape(form.username.data)
            email = form.email.data
            hashed_password = argon2.generate_password_hash(form.password.data)
            checked_user = UserInfo.query.filter_by(username=username_escaped, email=email).first()
            if checked_user:
                flash('Username or Email already exists', 'danger')
                return redirect(url_for('user_register.newregister'))
            
            try:
                session = db.session
                new_user = UserInfo(status=False, fname=fname, lname=lname,
                                        email=email, username=username_escaped,
                                        password=hashed_password,
                                        temp_password=pass_generator(12), trysend=0,
                                        id_discipline=3)
                session.add(new_user)
                session.commit()
                if app.config['SEND_EMAIL_REGISTER']:
                    send_confirmation_email(new_user.email)
                    flash('Te has registrado correctamente, Verifica tu correo para activar tu cuenta', 'info')
                print(f'[SUCCESS][REG][POST][INSERT] = {new_user.username} - Status:{new_user.status} - {new_user.email}')
                flash('Te has registrado correctamente', 'info')
                return redirect(url_for('user_login.login'))
            except Exception as e:
                print(f"Error registering user: {e}")
                flash('Error al registrarse. Inténtalo nuevamente.', 'error')
                return redirect(url_for('user_register.register'))

        else:
            flash('Invalid token!', 'error')
            return redirect(url_for('user_register.register'))
    return render_template('auth/register.html', form=form, text_data=text_data)