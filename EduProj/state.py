import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from EduProj import db
from EduProj.models import States, Matrices, Comments, Graphs

from werkzeug.security import check_password_hash, generate_password_hash

import logging
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Matrix:
    def __init__(self, rows, cols, data):
        self._rows = rows
        self._cols = cols
        self._data = data


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
    


bp = Blueprint('state', __name__, url_prefix="/state")

@bp.route('/read')
def readAll():
    error = None
    if request.method == "GET":
        result = States.query.all()
    return json.dumps(
        [
            {
                "id":row.id,
                "name": row.name
            } for row in result
        ]   
    )


@bp.route('/create', methods=('GET', 'POST'))
def create():
    error = None
    if request.method == 'POST':
        print(request.form)
        name = request.form["name"]
        order = request.form["obj_order"].split(";")

        obj_nums = int(request.form["obj_num"])
    
        comments = []

        try:
            comments.append(request.form["comment"])
        except:
            print("end reached")

        
        matrix_ids = []
        matrix_id = []
        graph_id = []
        for obj_num in range(obj_nums+1):
            
            if order[obj_num] == "M":

                rows = int(request.form["rows_"+str(obj_num)])
                cols = int(request.form["cols_"+str(obj_num)])
                data = ""
            
            
                for i in range(int(rows)):
                    for j in range(int(cols)):
                        data += request.form["data_"+str(obj_num)+"_"+str(i*cols+j)] + ","
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
                        #db.session.refresh()
                        matrix_id.append(matrix.id)
                        print("returned id"+str(matrix_id))
                    except db.IntegrityError:
                        error = f"Matrix already exists"
                else:
                    flash("Matrix create"+error)  
                    return redirect(url_for("matrix.display"))
            elif order[obj_num] == "C":
                minX = float(request.form["minXInput_"+str(obj_num)])
                minY = float(request.form["minYInput_"+str(obj_num)])
                maxX = float(request.form["maxXInput_"+str(obj_num)])
                maxY = float(request.form["maxYInput_"+str(obj_num)])
                degree = int(request.form["degreeInput_"+str(obj_num)])
                coefficients = request.form["coefficientInput_"+str(obj_num)].split(",")
            
            
                
                
                graph = Graphs(min_x = minX, max_x = maxX, min_y = minY, max_y = maxY, grad = degree, coeffizienten = coefficients)
                error = None
                if (not minX or 
                   not minY or 
                   not maxX or
                   not maxY or 
                   not degree or 
                   not coefficients):
                    error = "All Values need to be filled"
                if error is None:
                    try:
                        db.session.add(graph)
                        db.session.commit()
                        #db.session.refresh()
                        graph_id.append(graph.id)
                        print("returned id"+str(graph_id))
                    except db.IntegrityError:
                        error = f"Graph already exists"
                else:
                    flash("Graph create"+error)  
                    return redirect(url_for("graph.display"))

                


        matrix_id_string = ""
        graph_id_string = ""
        for id in matrix_id:
            matrix_id_string += str(id) + ","

        for id in graph_id:
            graph_id_string += str(id) + ","
       
        print(matrix_id)
        matrix_id_string = matrix_id_string[:-1]
        graph_id_string = graph_id_string[:-1]
        matrix_id = matrix_id_string
        graph_id = graph_id_string
        col_state = obj_nums
        
        

        logger.info(name)
       
        logger.info(matrix_id)

        if not name: 
            print(name)
            error = "Name must be filled"
        if (not matrix_id or 
           not graph_id): 
            print(matrix_id)
            error = "You need a reference object"

        if error is None:
            try: 
                matrix = Matrices.query.filter_by(id=matrix_id).first()
                
                state = States(name = name, matrixId = matrix_id, graphId = graph_id,col_state = col_state)

                db.session.add(state)
                db.session.commit()
                
                stateId = state.id

                for comment in comments:
                    if comment == '':
                        continue;
                    comment_obj = Comments(comment=comment, stateId=stateId)
                    db.session.add(comment_obj)
                db.session.commit()
                print(comments)

                flash("created")
                

            except Exception as e:
                
                flash("State create:"+e)
        else: 
            flash("Generic: "+error)

        
    return render_template("state/create.html", cols_page=2)

"""
currently has problems
"""
@bp.route("/read/<id>")
def read(id):
    
    returnMatrix = ""
    name = ""
    comment = ""
    data = ""    
    rows = 0    
    cols = 0    
    cols_page = 0
    
    
    state = States.query.filter_by(id=id).first()
    
    if not state is None:
        returnMatrix = state.matrixId
        name = state.name

        comments = Comments.query.filter_by(stateId = id).all()

       

        returnComments = []
        for comment in comments:
            commentlines = comment.comment.split(";")
            returnComments.append(commentlines)
        
        cols_page = state.col_state

        matrices = []

        for matrixId in returnMatrix.split(","):
            matrix = Matrices.query.filter_by(id=matrixId).first()
            matrices.append(matrix)

        returnMatrices = []
        if matrices is not None:
            for matrix in matrices: 
                
                rows = matrix.rows
                cols = matrix.rows
                data = matrix.data
              
        
                returnData = parseMatrixData(processMatrixData(data), rows, cols)
              
                currentMatrix = Matrix(rows, cols, returnData)
                returnMatrices.append(currentMatrix)
        
               
        
            return render_template("state/read.html", returnMatrices = returnMatrices ,matrix = returnData, cols = int(cols), rows = int(rows), comments=returnComments, name=name, cols_page=cols_page)
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
