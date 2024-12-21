from flask import redirect, flash, url_for, session, render_template, Blueprint
from pvadmin.models.pvadmin_model import PvAdminInfo
from dbconfig import app, db, database_status, email_ver_status, get_server_header
from options import time
from tokenauth import verify_jwt
from text import text_data


admin_dashboard = Blueprint('admin_dashboard', __name__)

####################################### Jinja2 #############################################

@admin_dashboard.route('/dashboard', methods=['GET'])
def pvadmindashboard():
    token = session.get('jwt_token')
    user_id = verify_jwt(token)
    db_state = database_status()
    mail_state = email_ver_status()
    header_status = get_server_header()
    if user_id:
        usuario_logueado = db.session.query(PvAdminInfo).get(user_id)
        if usuario_logueado:
            session['pvadmin_email'] = usuario_logueado.pvadmin_email
            app.logger.info(f'\033[1;32m[PVADMIN][DASHBOARD]\033[0m {usuario_logueado.pvadmin_email}')
            return render_template('pvadmin_templates/pvadmin_panel.html', 
                                   pvadmin_email=usuario_logueado.pvadmin_email,
                                   pvadmin_type=usuario_logueado.pvadmin_type, text_data=text_data, db_state=db_state, mail_state=mail_state, header_status=header_status)
    else:
        flash('Sesion Finalizada', 'info')
        return redirect(url_for('admin_login.pvadminlogin')) 

    
@admin_dashboard.route('/sign_out2')
def logout2():
    session.pop('jwt_token', None)
    response = redirect(url_for('admin_login.pvadminlogin'))
    response.delete_cookie('jwt_token')
    app.logger.info(f'\033[1;32m[PVADMIN][LOGOUT]\033[0m {time()}')
    return response

    