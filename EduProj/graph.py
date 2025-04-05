from flask import (
    Blueprint, flash, render_template, request, jsonify, abort
)
from . import db
from .models import Graphs
from EduProj.GraphGenerators import BasicGraph

import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bp = Blueprint('graph', __name__, url_prefix = "/graph")
"""
@bp.route("/", methods = ["GET"])
def getGraphs():
    db = get_db()
    graphs = db.execute(
        "SELECT * FROM graphs"
    ).fetchall()
    return jsonify(graphs)

@bp.route("/<id>", methods = ["GET"])
def getGraphbyId(id):
    db = get_db()
    graph = db.execute(
        "SELECT * FROM graphs "
        "WHERE id=?",
        (id,)
    ).fetchone()
    return jsonify(graph)

@bp.route("/", methods = ["POST"])
def postGraph():
    max_x = request.json.get("max_x")
    min_x = request.json.get("min_x")
    max_y = request.json.get("max_y")
    min_y = request.json.get("min_y")
    grad = request.json.get("grad")
    coef = request.json.get("coeffizienten")
    
    db = get_db()
    error = None
    
    if  id or  max_x is None or  min_x is None or  max_y is None or  min_y is None or  grad is None or  coef is None:
        error = "All Values need to be filled"
    
    if error is None:
        try:
            db.execute(
                "INSERT INTO graphs (max_x, min_x, max_y, min_y, grad, coeffizienten)"
                "VALUES (?, ?, ?, ?, ?, ?)",
                (max_x, min_x, max_y, min_y, grad, coef)
            )
            db.commit()
            return jsonify("added graph sucessfully")
        except db.IntegrityError:
            abort(500)
            
    else:
        abort(400,error)
            


@bp.route("/", methods = ["PUT"])
def updateGraph():
    id = request.json.get("id")
    max_x = request.json.get("max_x")
    min_x = request.json.get("min_x")
    max_y = request.json.get("max_y")
    min_y = request.json.get("min_y")
    grad = request.json.get("grad")
    coef = request.json.get("coeffizienten")
    
    db = get_db()
    error = None
    
    if  id or  max_x is None or  min_x is None or  max_y is None or  min_y is None or  grad is None or  coef is None:
        error = "All Values need to be filled"
    
    if error is None:
        try:
            db.execute(
                "UPDATE graphs SET max_x = ?, min_x = ?, max_y = ?, min_y = ?, grad = ?, coeffizienten = ? WHERE id = ?",
                (max_x, min_x, max_y, min_y, grad, coef,id)
            )
            db.commit()
            return jsonify("updated graph sucessfully")
        except db.IntegrityError:
            abort(500)
            
    else:
        abort(400,error)

@bp.route("/<id>", methods = ["PUT"])
def updateGraphbyId(id):
    max_x = request.json.get("max_x")
    min_x = request.json.get("min_x")
    max_y = request.json.get("max_y")
    min_y = request.json.get("min_y")
    grad = request.json.get("grad")
    coef = request.json.get("coeffizienten")
    
    db = get_db()
    error = None
    
    if  id or  max_x is None or  min_x is None or  max_y is None or  min_y is None or  grad is None or  coef is None:
        error = "All Values need to be filled"
    
    if error is None:
        try:
            db.execute(
                "UPDATE graphs SET max_x = ?, min_x = ?, max_y = ?, min_y = ?, grad = ?, coeffizienten = ? WHERE id = ?",
                (max_x, min_x, max_y, min_y, grad, coef, id)
            )
            db.commit()
            return jsonify("updated graph sucessfully")
        except db.IntegrityError:
            abort(500)
            
    else:
        abort(400,error)
        
@bp.route("/<id>", methods = ["DELETE"])
def deleteGraphbyId(id):
    
    db = get_db()
    
    try:
        db.execute(
            "DELETE FROM graphs WHERE id = ?",(id)
        )
        return jsonify("deleted graph sucessfully")
    except db.IntegrityError:
            abort(500)
"""

@bp.route("/read/<id>", methods = ["GET"])
def showGraph(id):    
    
    rawgraph = Graphs.query.filter_by(id=id).first()
    
    graphGenerator = BasicGraph.BasicGraph(rawgraph)
    graphProcessed = graphGenerator.generate()
    print(graphProcessed)
    
    return render_template("graph/read.html", graphData = graphProcessed, cols_page = 1)

@bp.route("/create", methods=["GET","POST"])
def createGraph():
    if request.method == "POST":
        max_x = int(request.form["max_x"])
        min_x = int(request.form["min_x"])
        max_y = int(request.form["max_y"])
        min_y = int(request.form["min_y"])
        grad = int(request.form["grad"])
        coef = request.form["coeffizienten"]
        
        graph = Graphs(max_x = max_x, min_x = min_x, max_y = max_y, min_y = min_y, grad = grad, coeffizienten = coef)
        error = None

        if  max_x is None or  min_x is None or  max_y is None or  min_y is None or  grad is None or  coef is None:
            print(max_x,min_x,max_y,min_y,grad,coef)
            error = "All Values need to be filled!"
            
        if error is None:
            try:
                db.session.add(graph)
                db.session.commit()
                flash("created")
            except db.IntegrityError:
                error = f"Graph already exists"
        else:
            abort(400,error)
        flash(error)
    return render_template("graph/create.html", cols_page = 1)

@bp.route("/update/<id>", methods=["GET","POST"])
def updateGraphHTML(id):
    if request.method == "POST":
        max_x = int(request.form["max_x"])
        min_x = int(request.form["min_x"])
        max_y = int(request.form["max_y"])
        min_y = int(request.form["min_y"])
        grad = int(request.form["grad"])
        coef = request.form["coeffizienten"]
        
        graph = Graphs.query.filter_by(id=id).first()
        
        error = None

        if  max_x is None or  min_x is None or  max_y is None or  min_y is None or  grad is None or  coef is None:
            print(max_x,min_x,max_y,min_y,grad,coef)
            error = "All Values need to be filled!"
            
        if error is None:
            try:
                graph.max_x = max_x
                graph.min_x = min_x
                graph.max_y = max_y
                graph.min_y = min_y
                graph.grad = grad
                graph.coeffizienten = coef
                db.session.commit()
                flash("Update successfull")
            except db.IntegrityError:
                error = f"Id doesn't exist"
        else:
            abort(400,error)
        flash(error)

    
    rawGraph = Graphs.query.filter_by(id=id).first()
        
    graphProcessed = jsonify(rawGraph)
    
    return render_template("graph/update.html", graphData = graphProcessed, cols_page = 1)