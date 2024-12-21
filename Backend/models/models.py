from dbconfig import db, app, mail
from sqlalchemy import ForeignKey
from itsdangerous import URLSafeTimedSerializer, BadSignature
from flask import url_for, flash, redirect
from flask_mail import Message
from itsdangerous import BadSignature, URLSafeSerializer

class UserInfo(db.Model):
    __tablename__ = 'profiles'
    id_profile = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    temp_password = db.Column(db.String(64), unique=True)
    fname = db.Column(db.String(50))
    lname = db.Column(db.String(50))
    email = db.Column(db.String(50))
    status = db.Column(db.Boolean, default=False)
    trysend = db.Column(db.Integer)
    id_discipline = db.Column(db.Integer, ForeignKey('disciplines.id_discipline'))
    def to_dict(self):
        user_dict = {
            'id_profile': self.id_profile,
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'temp_password': self.temp_password,
            'fname': self.fname,
            'lname':self.lname,
            'status': self.status,
            'trysend': self.trysend,
            'id_discipline': self.id_discipline
            
        }
        del user_dict['password']
        del user_dict['temp_password']
        return user_dict
    
    
def get_status(status):

  if status == 1:
      return "Activo"
  elif status == 0:
      return "Inactivo"
  else:
      return  status.status

#                       Status to True                        #

def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt='confirm_email')

def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt='confirm_email', max_age=expiration)
        return email
    except BadSignature:
        return None
    
 #Agregar funcion de checking de max_attempts   
def send_confirmation_email(user_email, enable_email_send = True):
  if enable_email_send:
    token = generate_confirmation_token(user_email)
    confirm_url = url_for('user_activate.confirm_email', token=token, _external=True)
    msg = Message('Confirma tu cuenta', sender='eloproyect@hotmail.com', recipients=[user_email])
    msg.body = f'Haz clic en el siguiente enlace para confirmar tu cuenta: {confirm_url}'
    mail.send(msg)    
  else:
    flash('Tu cuenta ha sido creada!', 'success')
    return redirect(url_for('index'))

###################  Reset Password   #####################

def generate_password_token(user_email):
  serializer = URLSafeSerializer('test')
  token = serializer.dumps(user_email)
  return token

def reset_token(token):
  serializer = URLSafeSerializer('test')
  try:
    user_email = serializer.loads(token)
    return user_email
  except BadSignature:
    return None
 
def send_password_email(user_email):
  token = generate_password_token(user_email)
  try:
    email = reset_token(token)
    if email:
      confirm_url = url_for('user_recovery.resetpassword', token=token, _external=True)
      msg = Message('Cambio de Password', sender='eloproyect@hotmail.com', recipients=[user_email])
      msg.body = f'Haz clic en el siguiente enlace para cambiar tu password: {confirm_url}'
      mail.send(msg)
      return True
    else:
      return False
  except BadSignature:
    return False
