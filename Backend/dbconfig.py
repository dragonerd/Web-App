from flask import g, request
import configparser
from flask_mail import Mail
from flask_wtf import CSRFProtect
from flask_cors import CORS
from flask_argon2 import Argon2
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from sqlalchemy import create_engine
from flask_talisman import Talisman

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5000"}})
argon2 = Argon2(app)
db = SQLAlchemy()
jwt = JWTManager(app)
csrf = CSRFProtect(app)


Talisman(app, content_security_policy={'default-src': "'self'", 
                                       'script-src': "'self' https://ajax.googleapis.com'", 
                                       'img-src': "'self' data:",
                                       'form-action':'http://127.0.0.1:5000',
                                       'frame-ancestors':"'self'"
                                       })

#BETA
#Revision de Headers
def get_server_header():
    with app.app_context():
        server = request.headers.get('Server')
        framework = request.headers.get('X-Powered-By')
        agent  = request.headers.get('User-Agent')
        app.logger.info(f'\033[31m HEADERS = {server} {framework} {agent} \033[0m')
        return server


#Carga de valores en data.ini
def load_config():
    config = configparser.ConfigParser()
    config.read('data.ini')
    return config
config = load_config()

#Instancias server
sqlalchemy_url = config['Database']['sqlalchemy.url']
app.config['SQLALCHEMY_DATABASE_URI'] = sqlalchemy_url

#Test de base de datos al iniciar el servidor
def test_db():
    try:
        engine = create_engine(sqlalchemy_url)
        engine.connect()
        app.logger.info(f'\033[1;32m[DB TEST] = SUCCESS\033[0m')
        return "En línea"
    except Exception as e:
        app.logger.info(f'\033[31m[DB TEST] = ERROR {e}\033[0m')
        return f"Fuera de línea: {str(e)}"
 
#Estatus de la base de datos para el panel PVADMIN  
def database_status():
    try:
        engine = create_engine(sqlalchemy_url)
        engine.connect()
        return "En línea"
    except Exception as e:
        return f"Fuera de línea: {str(e)}"

#DEFAULT VALUES
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECURITY_RECOVERABLE'] = True

#SECRET KEY 
SECRET_KEY = config['App']['SECRET_KEY']
app.config['SECRET_KEY'] = SECRET_KEY

#Variables Flask 
server_port = int(config['Server']['port'])
server_host = config['Server']['host']
print(f'\033[1;32mServer Flask Info: PORT:{server_port} - HOST {server_host}\033[0m')

#Debug Mode
debug_state = config.getboolean('App', 'DebugMode')
app.config['DEBUG'] = debug_state
valor_booleano = config.getboolean('App', 'DebugMode')
app.logger.info(f'\033[1;32m[CSRF][DEBUG MODE] = {debug_state}\033[0m')

#OTROS
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True

#WTFORMS SECRET KEY
WTF_SECRET_KEY = config['CSRF']['WTF_SECRET_KEY']
app.config['WTF_CSRF_SECRET_KEY'] = WTF_SECRET_KEY

enable_csrf = config['CSRF']['ENABLE_CSRF']
app.config['WTF_CSRF_ENABLED'] = True
valor_booleano = config.getboolean('CSRF', 'ENABLE_CSRF')
app.logger.info(f'\033[1;32m[CSRF][WTF_CSRF_ENABLE] = {enable_csrf}\033[0m')

#Mail Confirmation
app.config['MAIL_SERVER'] = config.get('MAIL', 'SERVER')
app.config['MAIL_PORT'] = config.getint('MAIL', 'PORT')
app.config['MAIL_USE_TLS'] = config.getboolean('MAIL', 'USE_TLS')
app.config['MAIL_USERNAME'] = config.get('MAIL', 'USERNAME')
app.config['MAIL_PASSWORD'] = config.get('MAIL', 'PASSWORD')
mail_server = app.config['MAIL_SERVER']
mail_port = app.config['MAIL_PORT']
mail = Mail(app)

#Mail Confirmation
mail_confirmation = config.getboolean('REGISTER', 'SEND_EMAIL_REGISTER')
app.config['SEND_EMAIL_REGISTER'] = mail_confirmation
app.logger.info(f'\033[1;32m[REGISTER][SEND_EMAIL_REGISTER] = {mail_confirmation}\033[0m')

#Estatus de verificacion de email para el panel PVADMIN         
def email_ver_status():
    return "Habilitado" if mail_confirmation else "Deshabilitado"


@app.teardown_appcontext
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
    
db.init_app(app)
csrf.init_app(app)
test_db()