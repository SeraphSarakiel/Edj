from flask_login import UserMixin
from EduProj import db
from dataclasses import dataclass


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

class StateArticle(db.Model):
    __tablename__ = 'state_article'
    id = db.Column(db.Integer, primary_key = True)
    stateId = db.Column(db.Integer, db.ForeignKey('states.id'))
    articleId = db.Column(db.Integer, db.ForeignKey('articles.id'))
    
class Articles(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    stateOrder = db.relationship('States', secondary = StateArticle.__table__, back_populates='articleId')
    

class StateGraphs(db.Model):
    __tablename__ = 'state_graphs'
    id = db.Column(db.Integer, primary_key = True)
    graphId = db.Column(db.Integer, db.ForeignKey('graphs.id'))
    stateId = db.Column(db.Integer, db.ForeignKey('states.id'))

class StateMatrix(db.Model):
    __tablename__ = 'state_matrix'
    id = db.Column(db.Integer, primary_key = True)
    matrixId = db.Column(db.Integer, db.ForeignKey('matrices.id'))
    stateId = db.Column(db.Integer, db.ForeignKey('states.id'))

class States(db.Model):
    __tablename__ = 'states'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    matrixId = db.relationship('Matrices', secondary=StateMatrix.__table__, back_populates='stateId') #db.Column(db.String(100))
    graphs = db.relationship('Graphs', secondary=StateGraphs.__table__, back_populates='states')
    articleId = db.relationship('Articles', secondary=StateArticle.__table__, back_populates='stateOrder')
    col_state = db.Column(db.Integer)
    order = db.Column(db.String(100))
    comments = db.relationship('Comments')
    
@dataclass
class Graphs(db.Model):
    __tablename__ = 'graphs'
    id = db.Column(db.Integer, primary_key=True)
    max_x = db.Column(db.Integer)
    min_x = db.Column(db.Integer)
    max_y = db.Column(db.Integer)
    min_y = db.Column(db.Integer)
    grad = db.Column(db.Integer)
    coeffizienten = db.Column(db.String(100))
    states = db.relationship('States', secondary=StateGraphs.__table__, back_populates='graphs')

class Matrices(db.Model):
    __tablename__ = 'matrices'
    id = db.Column(db.Integer, primary_key=True)
    rows = db.Column(db.Integer)
    cols = db.Column(db.Integer)
    data = db.Column(db.String(100))
    stateId = db.relationship('States', secondary=StateMatrix.__table__, back_populates='matrixId')
    
class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(1000))
    stateId = db.Column(db.Integer, db.ForeignKey('states.id'))