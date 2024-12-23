from flask_wtf import FlaskForm
from wtforms import  PasswordField, SubmitField, StringField
from wtforms.validators import DataRequired, length
from dbconfig import WTF_SECRET_KEY



class LoginForm(FlaskForm):
    username = StringField("ID de usuario:", validators=[DataRequired(), length(min=8, max=25)])
    password = PasswordField("Contrasenia:", validators=[DataRequired(), length(min=8, max=25)])
    submit = SubmitField('login')   
    class Meta:
        csrf = True
        csrf_secret = WTF_SECRET_KEY

def validate_csrf_and_form(form):
    if not form.validate_on_submit():

        return False
    return True
