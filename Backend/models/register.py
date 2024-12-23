from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, IntegerField
from wtforms.validators import DataRequired, length
from flask_wtf.csrf import CSRF
import random


#Formulario de validacion
class RegisterForm(FlaskForm):
    fname = StringField("Nombre:", validators=[DataRequired(), length(min=4, max=25)])
    lname = StringField("Apellido:", validators=[DataRequired(), length(min=4, max=25)])
    email = EmailField("Email:", validators=[DataRequired(), length(min=4, max=25)])
    username = StringField("ID de usuario:", validators=[DataRequired(), length(min=8, max=25)])
    password = PasswordField("Contrasenia:", validators=[DataRequired(), length(min=8, max=25)])
    temp_password = PasswordField('TESTFUNTION')
    trysend = IntegerField("trysend")
    submit = SubmitField("Registro")

def pass_generator(numero_char):
    mayus = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'Ñ', 'O', 'P', 'Q', 'R', 'S', 'T',
             'U', 'V', 'X', 'Y', 'Z']
    minus = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'ñ', 'o', 'p', 'q', 'r', 's', 't',
             'u', 'v', 'x', 'y', 'z']
    nums = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    chars = ['*', '+', '-', '/', '@', '_', '?', '!', '[', '{', '(', ')', '}', ']', ',', ';', '.', '>', '<', '~', '°',
             '^', '&', '$', '#', '"']
    
    characters = mayus + minus + nums + chars

    password = []

    for i in range(numero_char):
        char_random = random.choice(characters)
        password.append(char_random)

    password = "".join(password)

    return password

      
