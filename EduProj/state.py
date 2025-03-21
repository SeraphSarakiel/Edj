import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from EduProj.db import get_db

from werkzeug.security import check_password_hash, generate_password_hash

from EduProj.db import get_db

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Matrix:
    def __init__(self, rows, cols, data):
        self._rows = rows
        self._cols = cols
        self._data = data

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
    return [[float(data[i*3+j]) for i in range(rows)] for j in range(cols)]
    


bp = Blueprint('state', __name__, url_prefix="/state")

@bp.route('/create', methods=('GET', 'POST'))
def create():
    error = None
    if request.method == 'POST':
        name = request.form["name"]
        comment = request.form["comment"]
        matrix_id = request.form["matrix_id"]
        col_state = request.form["col_state"]

        logger.info(name)
        logger.info(comment)
        logger.info(matrix_id)

        if not name: 
            error = "Name must be filled"
        if not matrix_id: 
            error = "You need a reference object"

        if error is None:
            db = get_db()
            try: 
                matrix = db.execute(
                    "SELECT * FROM matrices "
                    "WHERE id = ?",
                    (matrix_id,)
                ).fetchone()

                db.execute(
                    "INSERT INTO states (name, comment, matrixId, col_state) " 
                    "VALUES (?, ?, ?, ?)",
                    (name,comment,matrix_id, col_state)
                );
                db.commit()
                flash("created")


            except Exception as e:
                flash(e)
        else: 
            flash(error)

        
    return render_template("state/create.html", cols_page=2)

@bp.route("/read/<id>")
def read(id):
    
    db = get_db()
    returnMatrix = ""
    name = ""
    comment = ""
    data = ""    
    rows = 0    
    cols = 0    
    cols_page = 0
    logging.info("ID")
    logging.info(id)
    
    state = db.execute(
        "SELECT * FROM states WHERE id = ?",
        (id)
    ).fetchone()
    
    if not state is None:
        returnMatrix = state["matrixId"]
        name = state["name"]
        comment = state["comment"]
        cols_page = state["col_state"]

        matrices = []

        for matrixId in returnMatrix.split(","):
            matrix = db.execute(
                "SELECT * FROM matrices WHERE id = ?",
                (matrixId,)
            ).fetchone()
            matrices.append(matrix)

        returnMatrices = []
        if matrices is not None:
            for matrix in matrices: 
                
                rows = matrix["rows"]
                cols = matrix["cols"]
                data = matrix["data"]
        
                returnData = parseMatrixData(processMatrixData(data), rows, cols)
                currentMatrix = Matrix(rows, cols, returnData)
                returnMatrices.append(currentMatrix)
        
            return render_template("state/read.html", returnMatrices = returnMatrices ,matrix = returnData, cols = int(cols), rows = int(rows), comment=comment, name=name, cols_page=cols_page)
        else:
            flash("No matrix with id" + str(returnMatrix))
            return redirect(url_for("matrix.create"))

    else: 
        flash("No State with this ID")
        return redirect(url_for("state.create"))

@bp.route("/next")
def next():
    session_order_split = session["order"].split(",")
    if session["current"] + 1 < len(session_order_split):
        session["current"] += 1
    else:
        session["current"] = len(session_order_split) - 1 

    
    return redirect(url_for("state.read", id=session_order_split[session["current"]]))
    

@bp.route("/previous")
def previous():
    session_order_split = session["order"].split(",")
    if session["current"] - 1 > 0 :
        session["current"] -= 1
    else: 
        session["current"] = 0
    return redirect(url_for("state.read", id=session_order_split[session["current"]]))
