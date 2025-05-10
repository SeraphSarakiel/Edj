import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)

from EduProj import db
from EduProj.models import States, Matrices, Comments, Graphs

from dataclasses import dataclass
from werkzeug.security import check_password_hash, generate_password_hash

import logging
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Graph:
    def __init__(self, max_x, min_x, max_y, min_y, koeffizient, degree, graphNumber):
        self.maxX = max_x
        self.minX = min_x
        self.maxY = max_y 
        self.minY = min_y 
        self.coefficient = koeffizient 
        self.degree = degree
        self.graphNumber = graphNumber

    def toJSON(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__, 
            sort_keys=True,
            indent=4)

class Matrix:
    def __init__(self, rows, cols, data):
        self._rows = rows
        self._cols = cols
        self._data = data


import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
        
def parseMatrixDataToString(rows, cols, requestForm, obj_num):
    data = ""
    for i in range(int(rows)):
        for j in range(int(cols)):
            data += requestForm["data_"+str(obj_num)+"_"+str(i*cols+j)] + ","
    return data[:-1]
    
    
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

        comments = []
        matrix_ids = []
        matrices = []
        graphs = []

        name = request.form["name"]

        #holds order of object types (C = Chart, M = Matrix)
        order = request.form["obj_type"].split(";")
        obj_nums = int(request.form["obj_num"])
        print("obj_nums")
        print(obj_nums)
        print("order")
        print(order)

        for obj_num in range(obj_nums+1):
            if order[obj_num] == "M":
                #Matrix Data definition
                rows = int(request.form["rows_"+str(obj_num)])
                cols = int(request.form["cols_"+str(obj_num)])
                data = parseMatrixDataToString(rows, cols, request.form, obj_num)
                dataNonString = data.split(",")
                
                
                #Data Base Object
                matrix = Matrices(rows = rows, cols = cols, data = data )
                print(matrix)

                #Value check
                if (not rows or 
                    not cols or 
                    not data):
                    error = "All Values need to be filled"
                #Rows and Cols size check
                if rows * cols != len(dataNonString):
                    error = "Invalid Matrix dimensions"
                #Datatype check
                for dataField in dataNonString:
                    try: 
                        float(dataField)
                    except e:
                        error = "Only numbers allowed" 

                if error is None:
                    try:
                        db.session.add(matrix)
                        db.session.commit()
                        
                        #keep created ids
                        matrices.append(matrix)
                    except db.IntegrityError:
                        error = f"Matrix already exists"
                    except e:
                        error = e
                else:
                    flash("Matrix create: "+error)  
                    return redirect(url_for("matrix.read"))
            elif order[obj_num] == "C":
                minX = float(request.form["minXInput_"+str(obj_num)])
                minY = float(request.form["minYInput_"+str(obj_num)])
                maxX = float(request.form["maxXInput_"+str(obj_num)])
                maxY = float(request.form["maxYInput_"+str(obj_num)])
                degree = int(request.form["degreeInput_"+str(obj_num)])
                coefficients = request.form["coefficientInput_"+str(obj_num)]
            
            
                graph = Graphs(min_x = minX, max_x = maxX, min_y = minY, max_y = maxY, grad = degree, coeffizienten = coefficients)
                error = None
                if (minX is None or 
                    minY is None or 
                    maxX is None or
                    maxY is None or 
                    degree is None or 
                    coefficients is None):
                    error = "All Values need to be filled"
                if error is None:
                    try:
                        db.session.add(graph)
                        
                        db.session.commit()
                        
                        graphs.append(graph)
                       
                    except db.IntegrityError:
                        error = f"Graph already exists"
                else:
                    flash("Graph create"+error)  
                    return redirect(url_for("graph.showGraph", id=1))

            #Comments for either Matrix or Chart
            try:
                comments.append(request.form["comment_"+obj_num])
            except:
                print("end reached")
                


       
    
        col_state = obj_nums
        
        

        logger.info(name)
       
        

        if not name: 
            print(name)
            error = "Name must be filled"
        if (not matrices and
           not graphs): 
            error = "You need a reference object"

        if error is None:
            try: 
                #matrix = Matrices.query.filter_by(id=matrix_id).first()
                orderString = ""
                for object in order: 
                    orderString += object + ","
                orderString = orderString[:-1]
                state = States(name = name, matrixId = matrices, graphs = graphs,col_state = col_state, order = orderString)

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
                
                flash("State create:"+str(e))
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
    returnData = ""
    
    state = States.query.filter_by(id=id).first()
    
    if not state is None:
        returnMatrix = state.matrixId
        returnGraphs = state.graphs
        name = state.name
        order = state.order
        comments = Comments.query.filter_by(stateId = id).all()
        returnGraphsObject = []
       

        returnComments = []
        for comment in comments:
            commentlines = comment.comment.split(";")
            returnComments.append(commentlines)
        
        cols_page = state.col_state

        matrices = []
        graphs = []

        for matrixId in returnMatrix:
            matrices.append(matrixId)

        for graphId in returnGraphs:
            graphs.append(graphId)

        

        returnMatrices = []
        if matrices is not None or graphs is not None:
            if matrices is not None:
                for matrix in matrices: 
                
                    rows = matrix.rows
                    cols = matrix.rows
                    data = matrix.data
            
                    returnData = parseMatrixData(processMatrixData(data), rows, cols)
                
                    currentMatrix = Matrix(rows, cols, returnData)
                    returnMatrices.append(currentMatrix)
            else:
                returnMatrices = []
            graphCounter = 0
            if graphs is not None:
                for graph in graphs:
                    returnGraphsObject.append(Graph(graph.max_x, 
                                              graph.min_x,
                                              graph.max_y,
                                              graph.min_y,
                                              graph.coeffizienten,
                                              graph.grad, 
                                              graphCounter).toJSON())
                    graphCounter += 1
            else: 
                returnGraphs = []
            

            return render_template("state/read.html", returnMatrices = returnMatrices,
                                                      returnGraphs = returnGraphsObject, 
                                                      matrix = returnData,
                                                      comments=returnComments, 
                                                      name=name, 
                                                      cols_page=cols_page, 
                                                      order=order)
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
