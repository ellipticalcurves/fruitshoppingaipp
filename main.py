from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
app.app_context().push()


class Todo(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  content = db.Column(db.String(200), nullable=False)
  completed = db.Column(db.Integer, default=0)
  date_created = db.Column(db.DateTime, default=datetime.utcnow)
  tip = db.Column(db.String, default="No tip")

  def __repr__(self):
    return '<Task %r>' % self.id


@app.route('/', methods=["POST", "GET"])
def index():
  emptyornot = ""
  foodtips = {
    "apple":
    "pink lady apples are usually crispy and sweet",
    "banana":
    """will ripen over time at home, take
             yellow if you want to eat immediately and green if you want to eat over the week""",
    "watermelon":
    "Check the mark near the top it should be yellow for sweetness and not white"
  }
  food = ["apple", "banana", "watermelon"]

  if request.method == 'POST':
    task_content = request.form['content'].strip()
    if not task_content:
      emptyornot = "Please type in something before adding."  # Error message for emp
      tasks = Todo.query.order_by(Todo.date_created).all()
      return render_template("index.html", tasks=tasks, emptyornot=emptyornot)
      
    new_task = Todo(content=task_content)
    if task_content in foodtips.keys():
      new_task.tip = foodtips[task_content]
      
    try:
      db.session.add(new_task)
      db.session.commit()
      return redirect("/")
    except:
      return "There was an error"

  elif request.method == "GET":
    tasks = Todo.query.order_by(Todo.date_created).all()
    # contents = [task.content for task in tasks]
    # available_tips = set(food).intersection(contents)
    # contents_indices = [contents.index(x) for x in available_tips]
    # for index in contents_indices:

    return render_template("index.html", tasks=tasks, emptyornot=emptyornot)

  else:
    tasks = Todo.query.order_by(Todo.date_created).all()
    for task in tasks:
      if task.content in foodtips:
        task.tip = foodtips[task.content]

    return render_template("index.html", tasks=tasks, emptyornot=emptyornot)


@app.route('/delete/<int:id>')
def delete(id):
  task_to_delete = Todo.query.get_or_404(id)
  try:
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect("/")
  except:
    return "Problem deleting"


@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
  task = Todo.query.get_or_404(id)
  if request.method == "POST":
    task.content = request.form["content"]
    try:
      db.session.commit()
      return redirect("/")
    except:
      return "error updating"
  else:
    return render_template("update.html", task=task)


@app.route("/search")
def search():
  pass


if __name__ == "__main__":
  db.create_all()
  app.run(debug=True, host='0.0.0.0', port=81)
