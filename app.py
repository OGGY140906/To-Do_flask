from flask import Flask, render_template, redirect, request, url_for
import sqlite3

app = Flask(__name__)

# Database initialization
connection = sqlite3.connect("ToDo.db")
cursor = connection.cursor()
cursor.execute(''' 
CREATE TABLE IF NOT EXISTS Tasks(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    priority TEXT NOT NULL,
    description TEXT,
    DueDate DATE
)
''')
connection.commit()
connection.close()

# Home route
@app.route('/', methods=['GET'])
def home():
    connection = sqlite3.connect("ToDo.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Tasks")
    tasks = cursor.fetchall()
    connection.close()
    return render_template('index.html', tasks=tasks)

# Add new task
@app.route('/add', methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        priority = request.form['priority']
        description = request.form['description']
        duedate = request.form['duedate']

        connection = sqlite3.connect('ToDo.db')
        cursor = connection.cursor()
        cursor.execute(''' 
            INSERT INTO Tasks(priority, description, DueDate)
            VALUES (?, ?, ?)
        ''', (priority, description, duedate))
        connection.commit()
        connection.close()
        return redirect(url_for('home'))

    return render_template('add.html')

# Update task
@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    if request.method == 'POST':
        priority = request.form['priority']
        description = request.form['description']
        duedate = request.form['duedate']

        connection = sqlite3.connect('ToDo.db')
        cursor = connection.cursor()
        cursor.execute('''
            UPDATE Tasks
            SET priority=?, description=?, DueDate=?
            WHERE id=?
        ''', (priority, description, duedate, id))
        connection.commit()
        connection.close()
        return redirect(url_for('home'))

    connection = sqlite3.connect('ToDo.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Tasks WHERE id=?', (id,))
    task = cursor.fetchone()
    connection.close()
    return render_template('update.html', task=task)

# ✅ Delete task
@app.route('/delete/<int:id>')
def delete(id):
    connection = sqlite3.connect('ToDo.db')
    cursor = connection.cursor()
    cursor.execute('DELETE FROM Tasks WHERE id=?', (id,))
    connection.commit()
    connection.close()
    return redirect(url_for('home'))

# ✅ Mark task as done (optional - removes the task)
@app.route('/done/<int:id>')
def mark_done(id):
    connection = sqlite3.connect('ToDo.db')
    cursor = connection.cursor()
    cursor.execute('DELETE FROM Tasks WHERE id=?', (id,))
    connection.commit()
    connection.close()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
