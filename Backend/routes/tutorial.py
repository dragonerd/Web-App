from flask import  render_template, Blueprint, session, redirect, url_for
from dbconfig import db
from tokenauth import verify_jwt
from text import text_data
from models.models import UserInfo
from models.disciplines import get_discipline
import datetime

training_mode = Blueprint('training_mode', __name__)


#Training Version 1.0.0 DONE
@training_mode.route('/training', methods=['GET'])
def training():
    token = session.get('jwt_token')
    user_id = verify_jwt(token)
    if user_id:
        usuario_logueado = db.session.query(UserInfo).get(user_id)
        if usuario_logueado:
            discipline = get_discipline(usuario_logueado.id_discipline)
            session['username'] = usuario_logueado.username
            current_time = datetime.datetime.now()
            print(f'[TEST] {usuario_logueado.username} - {discipline} - {current_time}')
            return render_template('training/training.html', 
                                   username=usuario_logueado.username, 
                                   fname=usuario_logueado.fname, 
                                   lname=usuario_logueado.lname, 
                                   email=usuario_logueado.email,
                                   discipline=discipline, text_data=text_data )
    else:
        return redirect(url_for('training'))    
