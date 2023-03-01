from flask import Flask, redirect, request, render_template, url_for
from dotenv import load_dotenv
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
load_dotenv()
app.config["SECRET_KEY"] = os.environ.get("MY_APP_SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///agenda.db'
db = SQLAlchemy(app)


# build db model
class List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<TodoItem {self.id}>'


app.app_context().push()
with app.app_context():
    db.create_all()


# add some initial tasks
# new_task = List(task="master ELB & ASG")
# db.session.add(new_task)
# db.session.commit()


# create a WTForm
class AddTodoForm(FlaskForm):
    task = StringField('Task', validators=[DataRequired()])
    submit = SubmitField('Add')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = AddTodoForm()
    if form.validate_on_submit():
        task = form.task.data
        todo_item = List(task=task)
        db.session.add(todo_item)
        db.session.commit()
        return redirect(url_for('index'))

    todo_items = List.query.all()
    return render_template('index.html', form=form, todo_items=todo_items)


@app.route('/delete/<int:todo_item_id>', methods=['POST'])
def delete(todo_item_id):
    todo_item = List.query.get_or_404(todo_item_id)
    db.session.delete(todo_item)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
