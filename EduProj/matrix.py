import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from EduProj import db
from EduProj.models import Matrices

from werkzeug.security import check_password_hash, generate_password_hash

import logging

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
    return [[float(data[i+j*rows]) for i in range(cols)] for j in range(rows)]

bp = Blueprint('matrix', __name__, url_prefix = "/matrix")



@bp.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        args = request.args.to_dict()
        rows = int(request.form["rows"])
        cols = int(request.form["cols"])
        data = ""
        #rows = request.form["rows"]
        #cols = request.form["cols"]
        for i in range(int(rows)):
            for j in range(int(cols)):
                data += request.form["data"+str(i*cols+j)] + ","
        data = data[:-1]
        logging.info(data)
        
        matrix = Matrices(rows = rows, cols = cols, data = data )
        error = None
        if not rows or not cols or not data:
            error = "All Values need to be filled"
        if error is None:
            try:
                db.session.add(matrix)
                db.session.commit()
                flash("created")
            except db.IntegrityError:
                error = f"Matrix already exists"
        else:
            return redirect(url_for("matrix.display"))
        flash(error)  
    return render_template("matrix/create.html", cols_page=1)




@bp.route("/read")
def read():
    matrices_processed = []

    matrices = Matrices.query.all()

    if len(matrices) >= 1:
        returnMatrices = []
        for matrix in matrices:
            # no assignment to sql lite row, so new dictionary object needs to be constructed
            matrices_processed.append({"id":matrix.id,"data":parseMatrixData(processMatrixData(matrix.data), matrix.rows, matrix.cols), "rows": matrix.rows, "cols": matrix.cols})
    
    
    return render_template("matrix/read.html", matrices=matrices_processed, cols_page=1)

@bp.route("/read/<id>")
def read_single(id):
    matrix = Matrices.query.filter_by(id=id).first()
    matrix_processed =  [{"id":matrix.id, "data":parseMatrixData(processMatrixData(matrix.data), matrix.rows, matrix.cols), "rows":matrix.rows, "cols":matrix.cols}]
    return render_template("matrix/read.html", matrices = matrix_processed, cols_page=1)

@bp.route("/update/<id>", methods=("GET", "POST"))
def update(id):
    if request.method == "POST":
        
        matrix = Matrices.query.filter_by(id=id).first()
        if matrix is not None:
            rowsOld = matrix.rows
            colsOld = matrix.cols
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
            matrix.rows = rows
            matrix.cols = cols
            matrix.data = data
            db.session.commit()
            flash("Update successfull")
            return redirect(url_for("matrix.update", id=id))
        else:
            flash("Id doesn't exist")
    elif request.method == "GET":
        matrix = Matrices.query.filter_by(id=id).first()
        data = matrix.data
        if matrix.rows * matrix.cols > len(data.split(",")):
            for i in range(matrix.rows * matrix.cols - len(data.split(","))):
                data += ",0"
        data = parseMatrixData(processMatrixData(data), matrix.rows, matrix.cols)
        return render_template("matrix/update.html", rows=matrix.rows, cols=matrix.cols, data=data, id=id, cols_page=1)

