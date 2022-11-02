from flask_login import UserMixin
from flask_sqlalchemy  import SQLAlchemy
from flask import Flask

from conf.definitions import get_key

app = Flask(__name__)
app.config['SECRET_KEY'] = get_key('data/app.key')
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///data/database/database.db"
db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16), unique=True)
    email = db.Column(db.String(320), unique=True)
    password = db.Column(db.String(80))