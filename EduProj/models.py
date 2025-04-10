from flask_login import UserMixin
from EduProj import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

class Matrices(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rows = db.Column(db.Integer)
    cols = db.Column(db.Integer)
    data = db.Column(db.String(100))
    
class Articles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    stateOrder = db.Column(db.String(100))

class States(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    matrixId = db.Column(db.String(100))
    graphId = db.Column(db.Integer, db.ForeignKey("graphs.id"), nullable=True)
    articleId = db.Column(db.Integer, db.ForeignKey("articles.id"),nullable=True)
    col_state = db.Column(db.Integer)
    
class Graphs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    max_x = db.Column(db.Integer)
    min_x = db.Column(db.Integer)
    max_y = db.Column(db.Integer)
    min_y = db.Column(db.Integer)
    grad = db.Column(db.Integer)
    coeffizienten = db.Column(db.String(100))
    
class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(1000))
    stateId = db.Column(db.Integer, db.ForeignKey("states.id"))