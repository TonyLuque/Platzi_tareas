from flask import Flask, request, make_response, redirect, render_template, url_for, flash 
from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField
from wtforms.validators import DataRequired
import pymongo

app = Flask(__name__)

app.config['SECRET_KEY'] = 'se debe generar un string seguro'

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client.platzi_tareas
collection = db.todo

class LoginForm(FlaskForm):
    tarea = StringField('Para hacer', validators=[DataRequired()])
    submit = SubmitField('Agregar')
    deleted = SubmitField('Borrar')


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)

@app.route('/')
def index():
    return make_response(redirect('/tareas'))

@app.route('/tareas', methods=['GET', 'POST', 'DELETE'])
def tareas():
    todos=[]
    for todo in collection.find():
        todos.append(todo)
    
    login_form = LoginForm()

    context={
        'todos': todos,
        'login_form': login_form
    }

    if request.method == 'POST':
        
        collection.insert_one({"name":login_form.tarea.data})

        flash('Tarea registrada')

        return redirect(url_for('index'))

    if request.method == 'DELETE':
        collection.delete_one({"name": login_form.tarea.data})
        print('Borrar')
        return redirect(url_for('index'))


    return render_template('index.html', **context)