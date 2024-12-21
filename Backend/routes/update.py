from flask import request, flash, render_template, redirect, url_for, Blueprint, session
from tokenauth import verify_jwt
from dbconfig import db
from models.models import UserInfo
from models.disciplines import UpdateDisciplineForm
from text import text_data


user_updateinfo = Blueprint('user_updateinfo', __name__)


@user_updateinfo.route('/update', methods=['GET','POST'])
def updatemyinfo():
     token = session.get('jwt_token')
     user_id = verify_jwt(token)
     form = UpdateDisciplineForm()
     if user_id:
        if request.method == 'POST':
            id_disciplines = request.form.get('disciplines')
            user = db.session.query(UserInfo).get(user_id)
            user.id_discipline = id_disciplines
            db.session.commit()
            flash('Datos Actualizados con exito', 'success')
            print(f'[SUCCESS][UPDATE INFO][POST] = {user.id_discipline}')
            return redirect(url_for('user_dashboard.dashboard'))
     else:
            flash('Error al cambiar los datos','error')
            return render_template('update/update.html', text_data=text_data, form=form)
     return render_template('update/update.html', text_data=text_data, form=form)