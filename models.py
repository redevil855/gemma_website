from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user_table'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    access = db.Column(db.Integer, default=0)
    building = db.Column(db.String(60), unique=False , nullable=False)

class Building(db.Model):
    __tablename__ = 'building_table'
    id = db.Column(db.Integer, primary_key=True)  
    department = db.Column(db.String(60),unique=True, nullable=False)
    
    