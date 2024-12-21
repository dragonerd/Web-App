from flask_wtf import FlaskForm
from wtforms import  PasswordField, SubmitField, StringField
from wtforms.validators import DataRequired, length
    
class NewPasswordForm(FlaskForm):
    username = StringField("ID de usuario:", validators=[DataRequired(), length(min=8, max=25)])
    password = PasswordField("Contrasenia:", validators=[DataRequired(), length(min=8, max=25)])
    submit = SubmitField("Actualizar")
      
  
    