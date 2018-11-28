from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt

from webapp.models import db
from webapp import app
from webapp.data import articles_base



POSTGRES = {
    'user': 'soapman',
    # 'pw': 'password',
    'db': 'flaskworkshop',
    'host': 'localhost',
    'port': '5432',
}

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s@%(host)s:%(port)s/%(db)s' % POSTGRES
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

def sql(rawSql, sqlVars={}):
    assert type(rawSql) == str
    assert type(sqlVars) == dict
    res = db.session.execute(rawSql, sqlVars)
    db.session.commit()
    return res

db.init_app(app)

articles_dict = articles_base()

@app.route('/')
def index():
    sql("INSERT INTO users(name) VALUES ('Mike Jorah') ON CONFLICT (name) DO NOTHING;")
    sql("INSERT INTO users(username) VALUES ('mike666') ON CONFLICT (name) DO NOTHING;")
    sql("INSERT INTO users(password) VALUES ('89756') ON CONFLICT (name) DO NOTHING;")
    sql("INSERT INTO users(email) VALUES ('sdf@sdf.com') ON CONFLICT (name) DO NOTHING;")
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/articles')
def articles():
    return render_template('articles.html', articles=articles_dict)

@app.route('/article/<int:id>')
def article(id):
    return render_template('article.html', article=articles_dict[id - 1])

class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=100)])
    username = StringField('Username', [validators.Length(min=4, max=30)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)

    if request.method == 'POST' and form.validate():
        render_template('register.html', form=form)

    return render_template('register.html', form=form)