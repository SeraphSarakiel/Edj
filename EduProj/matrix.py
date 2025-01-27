import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from EduProj.db import get_db

from werkzeug.security import check_password_hash, generate_password_hash

from EduProj.db import get_db

bp = Blueprint('matrix', __name__)

@bp.route('/create', methods=('GET', 'POST'))
def matrix():
    if request.method == 'POST':
        value1 = request.form["value1"]
        value2 = request.form["value2"]
        value3 = request.form["value3"]
        value4 = request.form["value4"]
        value5 = request.form["value5"]
        value6 = request.form["value6"]
        value7 = request.form["value7"]
        value8 = request.form["value8"]
        value9 = request.form["value9"]

        db = get_db()
        error = None

        if not value1:
            error = "All Values need to be filled"
        if not value2:
            error = "All Values need to be filled"

        if error is None:
            try:
                db.execute(
                    "INSERT INTO matrices (value1, value2, value3, value4, value5, value6, value7, value8, value9)"
                    "VALUES (?, ?, ?,?,?,?,?,?,?)",
                    (value1, value2, value3, value4,value5,value6,value7,value8,value9)
                )
                db.commit()
                flash("created")
            except db.IntegrityError:
                error = f"Matrix already exists"
        else:
            return redirect(url_for("matrix.display"))
        
        flash(error)
        
    return render_template("matrix/create.html")

@bp.route("/view", methods=("GET","POST"))
def index():
    db = get_db()
    
    matrices = db.execute(
        "SELECT * FROM matrices"
    ).fetchall()
    
    if len(matrices) > 1:
        returnMatrices = []
        for matrix in matrices:
            emptyMatrix = [[0 for i in range(3)] for j in range(3)]
            counter = 0 
            for i in range(3):
                for j in range(3):
                    emptyMatrix[i][j]=matrix[counter]
                    counter += 1
            returnMatrices.append(emptyMatrix)

    if request.method=="POST":
        value0 = request.form["value0"]
        value1 = request.form["value1"]
        value2 = request.form["value2"]
        value3 = request.form["value3"]
        value4 = request.form["value4"]
        value5 = request.form["value5"]
        value6 = request.form["value6"]
        value7 = request.form["value7"]
        value8 = request.form["value8"] 

        error = None
        if error is None:
            try:
                db.execute(
                    "UPDATE matrices "
                    "SET value1 = ?, value2 = ?,value3 = ?, value4 = ?,value5 = ?, value6 = ?,value7 = ?, value8 = ?, value9 = ?"
                    " WHERE id = 1",
                    (value0,value1, value2, value3, value4,value5,value6,value7,value8)
                )
                db.commit()
                flash("updated")
            except db.IntegrityError:
                error = f"Matrix already exists"
            return render_template("matrix/index.html", matrices=returnMatrices)
        else:
             return redirect(url_for("matrix.display"))
    else:
        return render_template("matrix/index.html", matrices=returnMatrices)

