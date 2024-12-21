from wtforms import SelectField, SubmitField
from dbconfig import db
from flask_wtf import FlaskForm

class DisciplineInfo(db.Model):
    __tablename__ = 'disciplines'
    id_discipline = db.Column(db.Integer, primary_key=True)
    discipline = db.Column(db.String(50))

class UpdateDisciplineForm(FlaskForm):
    discipline = SelectField('Disciplina', coerce=int)  # Coerce a int para obtener el id
    submit = SubmitField('Actualizar')
    
def get_discipline(discipline):

  if discipline is None:
      return "No Asignado"
  elif discipline==1:
      return "Just Dance"
  elif discipline==2:
      return "Beat Saber"
  elif discipline==3:
      return "Casual Player"
  else:
      return discipline.discipline
  