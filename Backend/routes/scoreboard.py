from flask import Blueprint, render_template
from text import text_data

user_scores = Blueprint('user_score', __name__)

@user_scores.route('/myscore', methods=['GET','POST'])
def scores():
        
    
 return render_template('scoreboard/records.html', text_data=text_data)

