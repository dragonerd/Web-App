
from pvadmin.filters.userfilter import get_all_users_data, total_accounts
from flask import redirect, request, flash, url_for, render_template, Blueprint, jsonify
from models.models import UserInfo
from text import text_data
from dbconfig import db, app
from routes.csrf import csrf_admin_status
from pvadmin.models.users import UsersForm
from options import time

admin_users = Blueprint('admin_users', __name__)

#OK
@admin_users.route('/all-users')
def show_all_users():
    app.logger.info(f'\033[1;32m[PVADMIN][ALL-USERS]\033[0m {time()}')
    user_data = get_all_users_data()
    total_users = int(total_accounts())
    return render_template('pvadmin_templates/pvadmin_users.html', user_data=user_data, total_users=total_users, text_data=text_data)

#OK
@admin_users.route('/all-usersv2')
def show_all_users_json():
    user_data = get_all_users_data()
    return jsonify(user_data)

#OK
@admin_users.route('/total-usersv2')
def total_users_json():
    user_accounts = total_accounts()
    return jsonify({'total_users': int(user_accounts)})

#OK
@admin_users.route('/delete-user', methods=['POST'])
def delete_user():
    form = UsersForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            users_ids = request.form.getlist('users_ids')
            app.logger.info('\033[1;32m[PVADMIN][USERS][DELETE][TOKEN]\033[0m %s', str(csrf_admin_status()))
        if users_ids: 
            session = db.session()
            try:
                for id_profile in users_ids:
                    user_entry = session.query(UserInfo).filter_by(id_profile=id_profile).first()

                    if user_entry:
                        session.delete(user_entry)
                session.commit()
                flash(f'El usuario {user_entry.username} ha sido eliminado con éxito', 'success') 
            except Exception as e:
                session.rollback()
                flash(f'Error al eliminar el usuario: {str(e)}', 'error')
        else:
            flash('No se seleccionaron usuarios para eliminar', 'warning')

        return redirect(url_for('admin_users.show_all_users'))
    else:
        
        pass  
    