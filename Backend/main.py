from flask import render_template, make_response
from dbconfig import app, db, mail, server_port, server_host
from flask_mail import Message
from text import text_data
from pvadmin.models.feed import FeedInfo
from pvadmin.routes.login import admin_login
from pvadmin.routes.dashboard import admin_dashboard
from pvadmin.routes.feed import admin_feed
from pvadmin.routes.users import admin_users
from pvadmin.routes.newpassword import admin_password
from pvadmin.routes.status import admin_update_status
from routes.login import user_login
from routes.dashboard import user_dashboard
from routes.recovery import user_recovery
from routes.newpassword import user_update
from routes.register import user_register
from routes.validate import user_activate
from routes.update import user_updateinfo
from routes.tutorial import training_mode
from routes.scoreboard import user_scores
from routes.feeds import feed
from routes.csrf import csrf_check_status, csrf_api
from routes.test import test
import webbrowser



@app.route('/')
@app.route('/index')
def index():
    """
    News Filtra de la base de datos la informacion de las noticias almacenadas.
    """
    news = db.session.query(FeedInfo).order_by(FeedInfo.date.desc()).limit(2).all() #Muestra los 2 primeros elementos mas actuales
    render = render_template('index.html', text_data=text_data, news=news)
    resp = make_response(render)
    app.logger.info('\033[1;32m[INDEX]\033[0m %s', str(csrf_check_status()))
    return resp

##################################         TEST          ############################################
app.register_blueprint(test, url_prefix='/test')

##################################       CSRF CHECK        ############################################
app.register_blueprint(csrf_api, url_prefix='/csrf_api')

##################################    Feed    ################################################
app.register_blueprint(feed, url_prefix='/feed')

##################################    Register    ################################################
app.register_blueprint(user_register, url_prefix='/register')

##################################    Validate User   ############################################
app.register_blueprint(user_activate, url_prefix='/validate')

##################################    Login     ##################################################
app.register_blueprint(user_login, url_prefix = '/login')

###############################    Dashboard - Logout   ##########################################
app.register_blueprint(user_dashboard, url_prefix = '/dashboard')

####################################    Training Mode   ##########################################
app.register_blueprint(training_mode, url_prefix = '/justdance')

################################    Recovery Password   ##########################################
app.register_blueprint(user_recovery, url_prefix = '/recoverypass')

################################    Update Password     ##########################################
app.register_blueprint(user_update, url_prefix = '/new_password')

################################      Update Info       ##########################################
app.register_blueprint(user_updateinfo, url_prefix = '/update')

################################      Records Info       ##########################################
app.register_blueprint(user_scores, url_prefix = '/scoreboard')

##################################   PvAdmin System - Login    ##################################################
#PvAdmin Login Version 1.0
app.register_blueprint(admin_login, url_prefix = '/pvadmin')

###################################   PvAdmin System  - Dashboard  ##############################################
#PvAdmin Panel Version 1.0
app.register_blueprint(admin_dashboard, url_prefix = '/pvadmin')

###################################   PvAdmin System - Feed System   ############################################
#PvAdmin Feed Version 1.0
app.register_blueprint(admin_feed, url_prefix ='/pvadmin')

####################################   PvAdmin System - SeekUsers System   ######################################
#PvAdmin SeekUsers Version 1.0
app.register_blueprint(admin_users, url_prefix='/pvadmin')

############################  PvAdmin System - SeekUsers System - Update Password   ###############################
#PvAdmin SeekUsers - Update Password Version 1.0
app.register_blueprint(admin_password, url_prefix='/pvadmin')

############################  PvAdmin System - SeekUsers System - Update Status   ###############################
#PvAdmin SeekUsers - Update Status Version 1.0
app.register_blueprint(admin_update_status, url_prefix='/pvadmin')


######################################   TEST     #################################################
@app.route('/testemail')
def enviar_correo():
    msg = Message('Asunto del correo', sender='eloproyect@hotmail.com', recipients=['bajamut12@gmail.com'])
    msg.body = 'Contenido del correo'
    mail.send(msg)
    return 'Correo enviado correctamente'


if __name__ == "__main__":
   webbrowser.open_new('http://127.0.0.1:5000/')
   webbrowser.open_new('http://127.0.0.1:5000/pvadmin/login')
   app.run(port=server_port, host=server_host)


