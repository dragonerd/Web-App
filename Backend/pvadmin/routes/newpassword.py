from flask import redirect, Blueprint, request, flash, url_for, render_template, session
from dbconfig import argon2, db, app
from tokenauth import verify_jwt
from pvadmin.models.users import UsersForm
from models.models import UserInfo
from text import text_data
from pvadmin.filters.userfilter import get_all_users_data


admin_password = Blueprint('admin_password', __name__)

@admin_password.route('/update_password/<user_id>', methods=['GET','POST'])
def updatepassword(user_id):
     token = session.get('jwt_token')
     admin_id = verify_jwt(token)
     form = UsersForm()
     if admin_id:
        user_data = get_all_users_data()
        if request.method == 'POST':
            new_password = form.password.data
            hashed_password = argon2.generate_password_hash(new_password)
            user = db.session.query(UserInfo).get(user_id)
            user.password = hashed_password
            user.temp_password = None
            db.session.commit()
            #app.logger.info(f'\033[1;32m   \033[0m')
            app.logger.info(f'\033[1;32m [PVADMIN][UPDATE INFO][PASSWORD]= Temp_Password Status : {user.temp_password} \033[0m')
            return redirect(url_for('admin_users.show_all_users'))
     else:
            flash('Error al cambiar los datos','error')
            return redirect(url_for('admin_users.show_all_users'))
     return render_template('pvadmin_templates/pvadmin_update_password.html', text_data=text_data, form=form, user_id=user_id, user_data=user_data)