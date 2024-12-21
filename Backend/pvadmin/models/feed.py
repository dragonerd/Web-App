from dbconfig import db
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, DateField
from wtforms.validators import DataRequired, length

db = SQLAlchemy()

class FeedInfo(db.Model):
    __tablename__ = 'feed'
    id_feed = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    date = db.Column(db.Date, nullable=False)
    author = db.Column(db.String, nullable=False)
    feed = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    def to_dict(self):
        return {
            'id_feed': self.id_feed,
            'date': self.date.strftime('%Y-%m-%d'), 
            'author': self.author,
            'feed': self.feed,
            'title': self.title
        }

class FeedForm(FlaskForm):
    date = DateField("Fecha")
    author = StringField("Autor")
    feed = StringField("Noticia")
    title = StringField("Titulo")
    submit = SubmitField("Agregar")