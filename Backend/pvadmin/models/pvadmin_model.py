from dbconfig import db
from flask_wtf import FlaskForm
from wtforms import  PasswordField, SubmitField, StringField, HiddenField
from wtforms.validators import DataRequired, length
    
class PvAdminInfo(db.Model):
    __tablename__ = 'pvadmin'
    id_pvadmin = db.Column(db.Integer, primary_key=True)
    pvadmin_password = db.Column(db.String(50))
    pvadmin_type = db.Column(db.Integer)
    pvadmin_email = db.Column(db.String(50))
    def to_dict(self):
        return {
            'id_pvadmin': self.id_pvadmin,
            'pvadmin_password': self.pvadmin_password,
            'pvadmin_type': self.pvadmin_type,
            'pvadmin_email': self.pvadmin_email,
        }
        
class PVLoginForm(FlaskForm):
    pvadmin_email = StringField("pvadmin_email:", validators=[DataRequired(), length(min=1, max=25)])
    pvadmin_password = PasswordField("pvadmin_password:", validators=[DataRequired(), length(min=1, max=25)])
    csrf_token = HiddenField()
    submit = SubmitField('login')

def validate_csrf_and_form(form):
    if not form.validate_on_submit():

        return False
    return True

 