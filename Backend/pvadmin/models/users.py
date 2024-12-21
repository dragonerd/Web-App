from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, length

class UsersForm(FlaskForm):
    username = StringField("ID de usuario:", validators=[DataRequired(), length(min=8, max=25)])
    password = PasswordField("Contrasenia:", validators=[DataRequired(), length(min=8, max=25)])
    status =  BooleanField("Status")
    submit = SubmitField("Actualizar")
      