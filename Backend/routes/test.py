from flask import Blueprint, flash, jsonify, request, render_template
from dbconfig import app
from text import text_data

@app.route("/test/users", methods=['GET'])
def users():
    return jsonify({"users": [{"id": 1, "name": "John Doe"},{"id": 2, "name": "Jane Doe"},{"id": 3, "name": "Bob Smith"},],})

test = Blueprint('test', __name__)  

@test.route("/csrfon", methods=['GET', 'POST']) 
def protected_form(): 
    if request.method == 'POST': 
        name = request.form['Name'] 
        return (' Hello ' + name + '!!!') 
    return render_template('develop/test1.html', text_data=text_data) 
  
@test.route("/csrfoff", methods=['GET', 'POST']) 
def unprotected_form(): 
    if request.method == 'POST': 
        name = request.form['Name'] 
        return (' Hello ' + name + '!!!') 
    return render_template('develop/test2.html', text_data=text_data) 