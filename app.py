from enum import unique
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# todoData = []
#find the current app path(directory name)
project_dir = os.path.dirname(os.path.abspath(__file__))

#creating the database file in the above found path
database_file = 'sqlite:///{}'.format(os.path.join(project_dir, 'todo.db'))

#connecting the database file(todo.db) to the SQLAlchemy dependecies
app.config["SQLALCHEMY_DATABASE_URI"] = database_file 
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Todo(db.Model):
    # id = db.Column(db.Integer, primary_key=True)
    todo = db.Column(db.String(50), unique=True, nullable=False, primary_key=True)

    def __repr__(self):
        return f'Todo: {self.todo}'

#created index
@app.route('/')
def index():
    return render_template('index.html', todos=todoData)


@app.route('/create-todo', methods=['POST'])
def create_todo():
    new_todo = request.form.get('new_todo')
    todoData.append(new_todo)
    print(todoData)
    return redirect(url_for('index'))

#created delete route
@app.route('/delete/<todo_item>')
def delete(todo_item):
    todoData.remove(todo_item)
    return redirect(url_for('index'))

#created update route
index_to_update= ''
@app.route('/update/<todo_item>', methods=['POST', 'GET'])
def update(todo_item):
    index = todoData.index(todo_item)
    global index_to_update
    index_to_update = index
    return render_template('update.html', todo_item = todo_item)

@app.route('/update_item', methods=['POST'])
def update_item():
    if request.method == 'POST':
        new_item = request.form.get('new_item')
        todoData[index_to_update] = new_item
    return redirect(url_for('index'))



if __name__ == "__main__":
    app.run(debug=True)