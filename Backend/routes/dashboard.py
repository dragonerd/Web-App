from flask import session, redirect, url_for, Blueprint, request, render_template
from tokenauth import verify_jwt
from text import text_data
from models.models import UserInfo
from models.disciplines import get_discipline
from dbconfig import db, app
import datetime
from routes.csrf import csrf_status, csrf_check_status
from options import time


user_dashboard = Blueprint('user_dashboard', __name__)

@user_dashboard.route('/dashboard', methods=["POST", "GET"])
def dashboard():
    app.logger.info('\033[1;32m[LOGIN]\033[31m->\033[0m\033[1;32m[DASHBOARD]\033[0m %s', str(csrf_check_status()))
    token = session.get('jwt_token')
    user_logged = session.get('username')
    user_id = verify_jwt(token)
    if user_id or user_logged :
        app.logger.info('\033[1;32m[DASHBOARD]\033[0m %s', str(csrf_status()))
        usuario_logueado = db.session.query(UserInfo).get(user_id)
        if usuario_logueado:
            discipline = get_discipline(usuario_logueado.id_discipline)
            session['username'] = usuario_logueado.username
            app.logger.info(f'\033[1;32m[DASHBOARD][SUCCESS] {usuario_logueado.username} - {discipline} -  {time()}\033[0m')
            return render_template('dashboard/dashboard.html', username=usuario_logueado.username, fname=usuario_logueado.fname, lname=usuario_logueado.lname, 
                                   email=usuario_logueado.email,
                                   discipline=discipline, text_data=text_data )
    else:
        return redirect(url_for('index'))

@user_dashboard.route('/sign_out')
def logout():
    session.pop('jwt_token', None)
    response = redirect(url_for('index'))
    response.delete_cookie('jwt_token')
    app.logger.info('\033[1;32m[DASHBOARD][LOGOUT]\033[0m %s', str(csrf_status()))
    return response
