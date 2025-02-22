import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from EduProj.db import get_db

from werkzeug.security import check_password_hash, generate_password_hash

import logging
from EduProj.db import get_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def processMatrixData(dataString):
    """
        Processes the matrix data
        dataString: input Data string with csv format, string

        return: Value float list, list
    """
    splitData = dataString.split(",")
    
    for value in splitData:
        value = float(value)
    return splitData

def parseMatrixData(data, rows, cols):
    """ Parses Matrix Data from string shape to double list
        data: matrix data string, string
        rows: matrix amount of rows, integer
        cols: matrix amount of cols, integer

        return: double list of matrix data

        exeptions: wrong data type
    """
    return [[float(data[i+j*3]) for i in range(cols)] for j in range(rows)]

bp = Blueprint('matrix', __name__, url_prefix = "/matrix")

@bp.route('/create', methods=('GET', 'POST'))
def matrix():
    if request.method == 'POST':
        rows = request.form["rows"]
        cols = request.form["cols"]
        data = request.form["data"]
        db = get_db()
        error = None
        if not rows or not cols or not data:
            error = "All Values need to be filled"
        if error is None:
            try:
                db.execute(
                    "INSERT INTO matrices (rows, cols, data)"
                    "VALUES (?, ?, ?)",
                    (rows, cols, data)
                )
                db.commit()
                flash("created")
            except db.IntegrityError:
                error = f"Matrix already exists"
        else:
            return redirect(url_for("matrix.display"))
        flash(error)  
    return render_template("matrix/create.html")

@bp.route("/read")
def index():
    db = get_db()
    matrices_processed = []

    matrices = db.execute(
        "SELECT * FROM matrices"
    ).fetchall()

    if len(matrices) >= 1:
        returnMatrices = []
        for matrix in matrices:
            # no assignment to sql lite row, so new dictionary object needs to be constructed
            matrices_processed.append({"id":matrix["id"],"data":parseMatrixData(processMatrixData(matrix["data"]), matrix["rows"], matrix["cols"]), "rows": matrix["rows"], "cols": matrix["cols"]})
    
    logger.info(matrices_processed)
    return render_template("matrix/index.html", matrices=matrices_processed)

@bp.route("/read/<id>")
def read(id):
    db = get_db()
    matrix = db.execute(
        "SELECT * FROM matrices" 
        " WHERE id=?",
        (id,)
    ).fetchone()
    matrix_processed =  [{"id":matrix["id"], "data":parseMatrixData(processMatrixData(matrix["data"]), matrix["rows"], matrix["cols"]), "rows":matrix["rows"], "cols":matrix["cols"]}]
    return render_template("matrix/index.html", matrices = matrix_processed)

@bp.route("/update/<id>", methods=("GET", "POST"))
def update(id):
    db = get_db()
    if request.method == "POST":
        
        matrix = db.execute("SELECT * FROM matrices "
                            "WHERE id = ?",
                            (id,)).fetchone()
        if matrix is not None:
            rowsOld = matrix["rows"]
            colsOld = matrix["cols"]
            rows = request.form["rows"]
            cols = request.form["cols"]
            data = ""
            for i in range(int(rows) * int(cols) - 1):
                if i < rowsOld * colsOld - 1:
                    cell = "data" + str(i)
                    data += request.form[cell] + ","
                else: 
                    data += "0,"

            data += request.form["data"+str(int(rows)*int(cols)-1)] if int(rowsOld)*int(colsOld) > int(rows)*int(cols) else "0"
                
            logging.info(data)
            db.execute("UPDATE matrices SET rows = ?, cols = ?, data = ? "
                       "WHERE id = ?",
                       (rows, cols, data, id))
            db.commit()
            flash("Update successfull")
            return redirect(url_for("matrix.update", id=id))
        else:
            flash("Id doesn't exist")
    elif request.method == "GET":
        matrix = db.execute("SELECT * FROM matrices WHERE id = ?",
                   (id,)).fetchone()
        data = matrix["data"]
        if matrix["rows"] * matrix["cols"] > len(data.split(",")):
            for i in range(matrix["rows"] * matrix["cols"]-len(data.split(","))):
                data += ",0"
        data = parseMatrixData(processMatrixData(data), matrix["rows"], matrix["cols"])
        return render_template("matrix/update.html", rows=matrix["rows"], cols=matrix["cols"], data=data, id=id)

