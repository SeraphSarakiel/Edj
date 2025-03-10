from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify, abort
)
from EduProj.db import get_db

import logging

import json

from EduProj.GraphGenerators import BasicGraph

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


bp = Blueprint('graph', __name__, url_prefix = "/graph")

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

    if not max_x or not min_x or not max_y or not min_y or not grad or not coef:
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
    
    if not id or not max_x or not min_x or not max_y or not min_y or not grad or not coef:
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
    
    if not id or not max_x or not min_x or not max_y or not min_y or not grad or not coef:
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

@bp.route("/display/<id>", methods = ["GET"])
def showGraph(id):
    db = get_db()

    rawgraph = db.execute(
        "SELECT * FROM graphs"
        " WHERE id=?",
        (id,)
    ).fetchone()
    
    graphGenerator = BasicGraph.BasicGraph(rawgraph)
    graphProcessed = graphGenerator.generate()
    
    return render_template("graph/index.html", graphData = json.dumps(graphProcessed))