
from flask import Blueprint, request, jsonify, make_response, session
from flask_wtf.csrf import generate_csrf, validate_csrf
from dbconfig import app
from flask_wtf import FlaskForm

class EmptyForm(FlaskForm):
    pass

#Funciones para revisar la creacion y almacenado del token CSRF en logs de terminal

########################################################################

def csrf_status():
    csrf_token = request.form.get('csrf_token')
    if csrf_token:
        return 'Token CSRF:{}'.format(csrf_token)
    else:
        return 'Token CSRF no encontrado'
    
def csrf_admin_status():
    csrf_token = request.form.get('csrf_token')
    if csrf_token:
        return '\033[1;32mToken CSRF:\033[0m {}'.format(csrf_token)
    else:
        return 'Token CSRF no encontrado.'
    
def csrf_check_status():
    csrf_token_form = request.form.get('csrf_token')
    csrf_token_session = session.get('csrf_token')
    csrf_token_cookie = request.cookies.get('csrf_token')
    if csrf_token_form:
        return 'Token CSRF Form:{}'.format(csrf_token_form)
    elif csrf_token_session:
        return 'Token CSRF Session:{}'.format(csrf_token_session)
    elif csrf_token_cookie:
        return 'Token CSRF Cookie:{}'.format(csrf_token_cookie)
    else:
        return 'Token CSRF no encontrado'
    
def csrf_session():
    csrf_token_session = session.get('csrf_token')
    if csrf_token_session:
        return 'Token CSRF Session:{}'.format(csrf_token_session)
    else:
        return 'Token CSRF no encontrado.'
    
def csrf_cookie():
    csrf_token_cookie = request.cookies.get('csrf_token')
    if csrf_token_cookie:
        return 'Token CSRF Cookie:{}'.format(csrf_token_cookie)
    else:
        return 'Token CSRF no encontrado.'

def csrf_form():
    csrf_token_form = request.form.get('csrf_token')
    if csrf_token_form:
        return 'Token CSRF Form:{}'.format(csrf_token_form)
    else:
        return 'Token CSRF no encontrado.'

    
########################################################################

csrf_api = Blueprint('csrf_api', __name__)

# VALIDAR TOKEN CSRF
###########################################################################

@csrf_api.route('/validate/csrf', methods=['POST', 'GET'])
def validate_csrf_all():
    csrf_token = request.cookies.get('csrf_token')
    if csrf_token:
        try:
            session_token = session.get('csrf_token')
            validate_csrf(data={'csrf_token': session_token}, csrf_token=csrf_token)
            return jsonify({'csrf_token': 'OK', 'csrf_token': csrf_token})
        except Exception as e:
            print(f"Error al validar el token CSRF: {e}")
            return jsonify({'error': 'Invalid CSRF token'}), 403
    else:
        return jsonify({'error': 'Missing CSRF token'}), 403
    
#Valida Token almacenado en Cookie 
    
@csrf_api.route('/validate/cookie/csrf', methods=['POST', 'GET'])
def validate_csrf_cookie():
    csrf_token = request.cookies.get('csrf_token')
    if csrf_token:
        try:
            validate_csrf(data={'csrf_token': csrf_token}, csrf_token=csrf_token)
            return jsonify({'csrf_token': 'OK', 'csrf_token': csrf_token})
        except Exception as e:
            print(f"Error al validar el token CSRF: {e}")
            return jsonify({'error': 'Invalid CSRF token'}), 403
    else:
        return jsonify({'error': 'Missing CSRF token'}), 403
    

#Valida Token almacenado en Session
    
@csrf_api.route('/validate/session/csrf', methods=['POST', 'GET'])
def validate_csrf_session():
    csrf_token_session = session.get('csrf_token')
    app.logger.info('\033[1;32m[LAST CSFR TOKEN] [Session] \033[0m %s', str(csrf_check_status()))
    if csrf_token_session:
        try:
            validate_csrf(csrf_token_session)
            return jsonify({'csrf_token': 'OK', 'csrf_token': csrf_token_session})
        except Exception as e:
            app.logger.info('\033[1;32m[CSFR TOKEN] [Session] [ERROR] \033[0m %s', str(csrf_check_status()))
            print(f"Error al validar el token CSRF: {e}")
            return jsonify({'error': 'Invalid CSRF token', 'Token Listed':csrf_token_session}), 403
    else:
        return jsonify({'error': 'Missing CSRF token'}), 403


# CREAR TOKEN CSRF
###########################################################################

# Token creado y almacenado en session
    
@csrf_api.route('/create/session/csrf', methods=['POST', 'GET'])
def create_csrf_session():
    app.logger.info('\033[1;32m[LAST CSFR TOKEN]\033[0m %s', str(csrf_check_status()))
    session.clear()
    csrf_token = generate_csrf()
    session['csrf_token'] = csrf_token
    app.logger.info('\033[1;32m[NEW TOKEN CSRF + SESSION]\033[0m %s', str(csrf_check_status()))
    return jsonify({'csrf_token with session':csrf_token})

# Token creado y almacenado en Cookie

@csrf_api.route('/create/cookie/csrf', methods=['POST', 'GET'])
def create_csrf_cookie():
    existing_token = request.cookies.get('csrf_token')
    if existing_token:
        response = make_response(jsonify({'success': 'Token CSRF eliminado'}))
        response.delete_cookie('csrf_token')
        return response
    app.logger.info('\033[1;32m[LAST CSFR TOKEN]\033[0m %s', str(csrf_check_status()))
    csrf_token = generate_csrf()
    app.logger.info('\033[1;32m[NEW TOKEN CSRF + COOKIE]\033[0m %s', str(csrf_check_status()))
    response = make_response(jsonify({'csrf_token with cookie': csrf_token}))
    response.set_cookie('csrf_token', csrf_token, httponly=True, secure=True)
    session.clear()
    return response

# Token creado y almacenado de session a cookie 

@csrf_api.route('/create/all/csrf', methods=['POST', 'GET'])
def create_all_csrf_type():
    app.logger.info('\033[1;32m[LAST CSFR TOKEN]\033[0m %s', str(csrf_check_status()))
    session.clear()
    csrf_token = generate_csrf()
    session['csrf_token'] = csrf_token
    app.logger.info('\033[1;32m[NEW TOKEN CSRF + SESSION]\033[0m %s', str(csrf_check_status()))
    response = make_response(jsonify({'csrf_token': csrf_token}))
    response.set_cookie('csrf_token', csrf_token, httponly=True, secure=True)
    csrf_token_cookie = request.cookies.get('csrf_token')
    app.logger.info(f'\033[1;32m[COOKIE + SESSION]\033[0m {csrf_token_cookie}')
    return response



# BORRAR TOKENS CSRF
###########################################################################

# Borra Tosos los tokens en session y cookie

@csrf_api.route('/delete/csrf/all', methods=['POST', 'GET'])
def delete_all_csrf():
    app.logger.info('\033[1;32m[TOKEN COOKIE]\033[0m %s', str(csrf_cookie()))
    app.logger.info('\033[1;32m[TOKEN SESSION]\033[0m %s', str(csrf_session()))
    session.clear()
    response = make_response(jsonify({'message': 'Token CSRF eliminados'}))
    response.delete_cookie('csrf_token')
    return response

# Borra el token almacenado en session

@csrf_api.route('/delete/csrf/session', methods=['POST', 'GET'])
def delete_session_csrf():
    app.logger.info('\033[1;32m[TOKEN SESSION]\033[0m %s', str(csrf_session()))
    session.clear()
    return jsonify({'success':'Token Session deleted'})

# Borra el token almacenado en cookie

@csrf_api.route('/delete/csrf/cookie', methods=['POST', 'GET'])
def delete_cookie_csrf():
    app.logger.info('\033[1;32m[TOKEN COOKIE]\033[0m %s', str(csrf_cookie()))
    response = make_response(jsonify({'success': 'Token Cookie Deteled'}))
    response.delete_cookie('csrf_token')
    return response

# REVISAR TOKENS CSRF
###########################################################################
@csrf_api.route('/check/csrf/all', methods=['POST', 'GET'])
def check_all_csrf():
    csrf_token_session = session.get('csrf_token')
    csrf_token_cookie = request.cookies.get('csrf_token')
    response = make_response(jsonify({'Token CSRF Session': csrf_token_session, 'Token CSRF Cookie':csrf_token_cookie}))
    return response


# REVISAR TOKEN CSRF
###########################################################################

@csrf_api.route('/check/csrf', methods=['POST', 'GET'])
def check_csrf_cookie():
    csrf_token_from_cookie = request.cookies.get('csrf_token')
    session_token = session.get('csrf_token')
    return jsonify({'Token from cookie': csrf_token_from_cookie, 'Token from session': session_token })




