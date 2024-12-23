from flask_wtf import FlaskForm
from wtforms import  PasswordField, SubmitField, StringField, EmailField
from wtforms.validators import DataRequired, length

class ResetPasswordForm(FlaskForm):
    fname = StringField("Nombre:", validators=[DataRequired(), length(min=4, max=25)])
    lname = StringField("Apellido:", validators=[DataRequired(), length(min=4, max=25)])
    email = EmailField("Email:", validators=[DataRequired(), length(min=4, max=25)])
    username = StringField("ID de usuario:", validators=[DataRequired(), length(min=8, max=25)])
    password = PasswordField("Contrasenia:", validators=[DataRequired(), length(min=8, max=25)])
    temp_password = PasswordField("Contrasenia:", validators=[DataRequired(), length(min=8, max=25)])
    submit = SubmitField("Registro")

