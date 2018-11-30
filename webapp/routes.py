from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from passlib.hash import sha256_crypt
from functools import wraps

from webapp import app, db
from webapp.models import User, Article
from webapp.forms import RegisterForm, ArticleForm

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, please login', 'danger')
            return redirect(url_for('login'))
    return wrap

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_candidate = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user:
            password = user.password
            if sha256_crypt.verify(password_candidate, password):
                session['logged_in'] = True
                session['username'] = username

                flash('You are logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid password'
                return render_template('login.html', error=error)
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)
    return render_template('login.html')

@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are logged out', 'success')
    return redirect(url_for('login'))

@app.route('/articles')
def articles():
    articles = Article.query.all()

    if articles != []:
        return render_template('articles.html', articles=articles)
    else:
        msg = 'No articles found'
        return render_template('articles.html', msg=msg)

@app.route('/article/<int:id>')
def article(id):
    article = Article.query.filter_by(id=id).first()

    if article:
        return render_template('article.html', article=article)
    else:
        flash('No such article')
        return redirect(url_for('articles'))

@app.route('/add_article', methods=['GET', 'POST'])
@is_logged_in
def add_article():
    form = ArticleForm(request.form)

    if request.method == 'POST' and form.validate():
        title = form.title.data
        body = form.body.data

        user_id = User.query.filter_by(username=session['username']).first().id
        article = Article(title=title, body=body, user_id=user_id)
        db.session.add(article)
        db.session.commit()

        flash('Article created', 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_article.html', form=form)

@app.route('/edit_article/<int:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_article(id):
    article = Article.query.filter_by(id=id).first()

    form = ArticleForm(request.form)

    form.title.data = article.title
    form.body.data = article.body

    if request.method == 'POST' and form.validate():
        title = request.form['title']
        body = request.form['body']

        article.title = title
        article.body = body

        db.session.commit()

        flash('Article created', 'success')
        return redirect(url_for('dashboard'))

    return render_template('edit_article.html', form=form)

@app.route('/delete_article/<int:id>', methods = ['POST'])
@is_logged_in
def delete_article(id):
    article = Article.query.filter_by(id=id).first()

    db.session.delete(article)
    db.session.commit()

    flash('Article deleted', 'success')
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
@is_logged_in
def dashboard():
    articles = Article.query.all()

    if articles != []:
        return render_template('dashboard.html', articles=articles)
    else:
        msg = 'No articles found'
        return render_template('dashboard.html', msg=msg)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)

    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        user = User(name=name, email=email, username=username, password=password)
        db.session.add(user)
        db.session.commit()

        flash('You are now registered and can log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)