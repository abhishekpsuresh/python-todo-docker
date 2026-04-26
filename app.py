from flask import Flask, request, redirect, url_for, render_template_string

app = Flask(__name__)

tasks = []

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Todo App</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-dark text-white">

<div class="container mt-5">
    <h1 class="text-center mb-4">📝 To-Do List</h1>

    <form method="POST" action="/add" class="d-flex mb-3">
        <input type="text" name="task" class="form-control me-2" placeholder="Enter task" required>
        <button type="submit" class="btn btn-success">Add</button>
    </form>

    <ul class="list-group">
        {% for task in tasks %}
        <li class="list-group-item d-flex justify-content-between align-items-center">
            
            {% if task.done %}
                <span style="text-decoration: line-through;">{{task.text}}</span>
            {% else %}
                <span>{{task.text}}</span>
            {% endif %}

            <div>
                <a href="/toggle/{{loop.index0}}" class="btn btn-warning btn-sm">✔</a>
                <a href="/edit/{{loop.index0}}" class="btn btn-primary btn-sm">Edit</a>
                <a href="/delete/{{loop.index0}}" class="btn btn-danger btn-sm">Delete</a>
            </div>

        </li>
        {% endfor %}
    </ul>
</div>

</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML, tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    task_text = request.form['task']
    tasks.append({"text": task_text, "done": False})
    return redirect(url_for('home'))

@app.route('/delete/<int:index>')
def delete(index):
    tasks.pop(index)
    return redirect(url_for('home'))

@app.route('/toggle/<int:index>')
def toggle(index):
    tasks[index]['done'] = not tasks[index]['done']
    return redirect(url_for('home'))

@app.route('/edit/<int:index>', methods=['GET', 'POST'])
def edit(index):
    if request.method == 'POST':
        tasks[index]['text'] = request.form['task']
        return redirect(url_for('home'))

    return f'''
    <form method="POST">
        <input type="text" name="task" value="{tasks[index]['text']}" required>
        <button type="submit">Save</button>
    </form>
    '''

app.run(host='0.0.0.0', port=5000)