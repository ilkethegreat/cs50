from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class dolist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    dateCreated = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        tasks = dolist.query.order_by(dolist.dateCreated).all()
        return render_template("index.html", tasks=tasks)
    else:
        taskContent = request.form['content']
        newTask = dolist(content=taskContent)

        try:
            db.session.add(newTask)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an error adding the task."

@app.route('/delete/<int:id>')
def delete(id):
    taskDeleted = dolist.query.get_or_404(id)

    try:
        db.session.delete(taskDeleted)
        db.session.commit()
        return redirect('/')
    except:
        return "There was an error deleting the task."

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = dolist.query.get_or_404(id)
    if request.method == 'GET':
        return render_template('update.html', task=task)
    else:
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was an error updating the task."



if __name__ == "__main__":
    app.run(debug=True)