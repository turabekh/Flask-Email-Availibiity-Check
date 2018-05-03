from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required, Email
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.secret_key = 'development key'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'test.sqlite')

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64),
                      nullable=False, unique=True, index=True)

class UserForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Email()])
    submit = SubmitField("submit")

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/success')
def success():
    return render_template("success.html")
@app.route('/adduser', methods=["GET", "POST"])
def add_user():
    form = UserForm()
    if form.validate_on_submit():
        db.create_all() #creates table if not exists
        # queries the user with submitted email input if exists returns back to the form
        user = User.query.filter_by(email = form.email.data).first()
        if user:
            return redirect(url_for('add_user'))
        email = form.email.data 
        user = User(email=email)
        db.session.add(user)
        db.session.commit() 
        return redirect(url_for('success'))
    return render_template("users.html", form=form)


@app.route('/check')
def check():
    # get email from query string
    email = request.args.get("EmailAddress")
    user = User.query.filter_by(email=email).first()
    if user is None:
        return jsonify(xhr="eror"), 400
    if not user is None:
        response = jsonify(email)
        return response

    

if __name__ == "__main__":
    app.run(debug=True)