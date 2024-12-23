from flask import request, flash, render_template, redirect, url_for, Blueprint, session
from tokenauth import verify_jwt
from dbconfig import db, app
from models.models import UserInfo
from pvadmin.models.users import UsersForm
from text import text_data

admin_update_status = Blueprint('admin_update_status', __name__)

@admin_update_status.route('/update/<user_id>', methods=['GET','POST'])
def updatestatus(user_id):
     token = session.get('jwt_token')
     admin_id = verify_jwt(token)
     form = UsersForm()
     if admin_id:
        if request.method == 'POST':
            status = request.form.get('status')
            user = db.session.query(UserInfo).get(user_id)
            if status == "1":
                user.status = True
            elif status == "0":
                user.status = False
            db.session.commit()
            app.logger.info(f'\033[1;32m [PVADMIN][UPDATE INFO][STATUS]= {user.status} \033[0m')
            return redirect(url_for('admin_users.show_all_users', form=form, user_id=user_id))
     else:
            flash('Error al cambiar los datos','error')
            return render_template('pvadmin_templates/pvadmin_status.html', text_data=text_data, form=form, user_id=user_id)
     return render_template('pvadmin_templates/pvadmin_status.html', text_data=text_data, form=form, user_id=user_id)