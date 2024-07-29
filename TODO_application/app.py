from flask import Flask, render_template, redirect, url_for, request
from flask_mysqldb import MySQL
import os

app = Flask(__name__)

# Configure MySQL
app.config['SECRET_KEY'] = "Vijay@006"
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Vijay@006'
app.config['MYSQL_DB'] = 'tasks'

mysql = MySQL(app)
static_url_path = '/static'
@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tasks")
    tasks = cur.fetchall()
    cur.close()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO tasks (title, description) VALUES (%s, %s)", (title, description))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))
    return render_template('add_task.html')

@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE tasks SET completed = 1 WHERE id = %s", (task_id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
