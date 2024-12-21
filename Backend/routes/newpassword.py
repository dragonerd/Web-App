from flask import redirect, Blueprint, request, flash, url_for, render_template, session
from dbconfig import argon2, db
from tokenauth import verify_jwt
from models.newpassword import NewPasswordForm
from models.models import UserInfo
from text import text_data
import datetime


user_update = Blueprint('user_update', __name__)

@user_update.route('/new_password', methods=['GET','POST'])
def newpassword():
     token = session.get('jwt_token')
     user_id = verify_jwt(token)
     form = NewPasswordForm()
     if user_id:
        if request.method == 'POST':
            new_password = form.password.data
            hashed_password = argon2.generate_password_hash(new_password)
            user = db.session.query(UserInfo).get(user_id)
            user.password = hashed_password
            user.temp_password = None
            db.session.commit()
            print(f'[SUCCESS][LOST PASS][POST][INSERT] = Temp_Password Status : {user.temp_password}')
            return redirect(url_for('user_update.clearsession'))
     else:
            flash('Error al cambiar los datos','error')
            return redirect(url_for('user_update.newpassword'))
     return render_template('newpassword/newpassword.html', text_data=text_data, form=form)
 
@user_update.route('/update_password')
def clearsession():
    session.clear()
    current_time = datetime.datetime.now()
    response = redirect(url_for('index'))
    response.delete_cookie('jwt_token')
    flash('Contraseña restablecida con éxito', 'success')
    print(f'[SUCCESS][LOGOUT] {current_time}')
    return response
 