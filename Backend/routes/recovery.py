from flask import request, flash, render_template, Blueprint, redirect, url_for
from dbconfig import mail, db
from models.resetpassword import ResetPasswordForm
from models.models import UserInfo, send_password_email, reset_token
from models.register import pass_generator
from text import text_data
from flask_mail import Message


user_recovery = Blueprint('user_recovery', __name__)

###############################    Request Send Reset Password    ######################################

@user_recovery.route('/recovery', methods=['POST', 'GET'])
def recovery():
    form = ResetPasswordForm()
    if request.method == 'POST':
        email = form.email.data
        user = db.session.query(UserInfo).filter_by(email=email).first()
        if user:
                send_password_email(email)
                print(f'[SUCCESS][REC][POST][SELECT] Email Send to: {email}')
                flash('Se ha enviado un correo para restablecer su contraseña.', 'success')
                return render_template('login/login.html', text_data=text_data, form=form)
        else:
                print(f'[ERROR][REC][POST][SELECT]= No se encontraron registros para el correo electrónico: {email}')
                flash('Los datos suministrados no poseen registros en la base de datos.', 'error')
                return render_template('recovery/recovery.html', text_data=text_data, form=form)
    return render_template('recovery/recovery.html', text_data=text_data, form=form)



##################################    Reset password    ##################################################

@user_recovery.route('/resetpassword/<token>', methods=['GET', 'POST'])
def resetpassword(token):
    user_email = reset_token(token)

    if user_email is None:
        flash('El token es inválido o ha expirado.', 'error')
        return render_template('index.html', token=token, text_data=text_data)

    else:
         nueva_password = pass_generator(12)
         new_pass = nueva_password
         if new_pass:
               user = db.session.query(UserInfo).filter_by(email=user_email).first()
               user.temp_password = new_pass
               db.session.commit()
               msg = Message('Cambio de Password', sender='eloproyect@hotmail.com', recipients=[user_email])
               msg.body = f'Hola! este es tu codigo temporal: [ {new_pass} ]  Recuerda que tiene una duracion de 1 hora'
               mail.send(msg)
               print(f'[SUCCESS][LOST PASS][POST][INSERT] {new_pass} - {user.email}')
               flash('Se ha enviado un codigo temporal a tu correo!', 'success')
               return redirect(url_for('user_login.login'))         

         else:
            flash('Error al actualizar la contraseña del usuario.', 'error')
            return redirect(url_for('index'))
