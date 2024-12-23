import jwt
from Backend.dbconfig import SECRET_KEY
from flask import current_app

def generate_jwt(user_id):
    payload = {'user_id': user_id}
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def verify_jwt(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user_id = payload['user_id']
        return user_id
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):

     return None

def generar_token(email):
    return jwt.encode({"email": email}, current_app.config["SECRET_KEY"], algorithm="HS256")
