from flask import redirect, request, flash, url_for, session, make_response, render_template, Blueprint
from pvadmin.models.pvadmin_model import PvAdminInfo, PVLoginForm, validate_csrf_and_form
from dbconfig import app, db
from tokenauth import generate_jwt
from text import text_data
from routes.csrf import csrf_admin_status
from options import time

admin_login = Blueprint('admin_login', __name__)

#PvAdmin Login Version 1.0

@admin_login.route('/login', methods=['GET','POST'])
def pvadminlogin():
    form = PVLoginForm()
    if request.method == 'POST':
        if validate_csrf_and_form(form):
            email = form.pvadmin_email.data
            password = form.pvadmin_password.data
            user = db.session.query(PvAdminInfo).filter_by(pvadmin_email=email, pvadmin_password=password).first()
        if user:
            if not user.pvadmin_type:
                app.logger.error(f'\033[31m[PVADMIN][LOGIN]\031[0m Level:{user.pvadmin_type} | {user.pvadmin_email} | {time()}')
                flash('No tienes Privilegios para poder ingresar', 'error')
                return redirect(url_for('admin_login.pvadminlogin'))
        if user and user.pvadmin_password  == password :
            jwt_token = generate_jwt(user.id_pvadmin)
            session['jwt_token'] = jwt_token
            app.logger.info(f'[SUCCESS][PVADMIN - LOGIN] Level:{user.pvadmin_type} | {user.pvadmin_email} | {time()}')
            app.logger.info('\033[1;32m[PVADMIN][LOGIN][TOKEN]\033[0m %s {}', str(csrf_admin_status()))
            flash(f'Bienvenido, usa las herramientas con precaucion y notifica al administrador ante problemas de backend', 'success')
            response = make_response(redirect(url_for('admin_dashboard.pvadmindashboard')))
            return response
        else:
            app.logger.error(f'[PVADMIN][ERROR][LOGIN] {email}')
            flash('Los datos ingresados son incorrectos', 'error')
            return render_template('pvadmin_templates/pvadmin_login.html', text_data=text_data, form=form)
        
    return render_template('pvadmin_templates/pvadmin_login.html', text_data=text_data, form=form)

