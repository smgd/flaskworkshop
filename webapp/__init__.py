from flask import Flask

app = Flask(__name__, template_folder='../templates')

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskworkshop'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

from webapp import routes