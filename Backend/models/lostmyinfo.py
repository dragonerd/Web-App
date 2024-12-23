#Wtforms
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired, length
from flask_wtf import FlaskForm
import pyotp

#Flask Wtforms

class RecoveryForm(FlaskForm):
    fname = StringField("Nombre:", validators=[DataRequired(), length(min=4, max=25)])
    lname = StringField("Apellido:", validators=[DataRequired(), length(min=4, max=25)])
    email = EmailField("Email:", validators=[DataRequired(), length(min=4, max=25)])
    username = StringField("ID de usuario:", validators=[DataRequired(), length(min=4, max=25)])
    password = PasswordField("Contrasenia:", validators=[DataRequired(), length(min=4, max=25)])
    submit = SubmitField("Registro")
    

# Genera una contraseña aleatoria de 10 caracteres
random_password = pyotp.random_base32(length=40)