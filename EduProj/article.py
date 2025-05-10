import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, make_response
)

from EduProj import db

from EduProj.models import Articles, States

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
    return [[float(data[i+j*3]) for i in range(rows)] for j in range(cols)]

bp = Blueprint('article', __name__)

@bp.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        name = request.form["name"]
        order = request.form["order"].split(",")
        stateOrder = []
        for state in order:
            stateObject = States.query.filter_by(id=state).first()
            stateOrder.append(stateObject)
        
        



        error = None

        if not name or not order:
            error = "All Values need to be filled"

        if error is None:
            new_article = Articles(name= name, stateOrder= stateOrder)
            db.session.add(new_article)
            db.session.commit()
            flash("article created")
        else:
            return redirect(url_for("article.display"))
        
        flash(error)
        
    return render_template("article/create.html", cols_page=1, url=url_for("state.readAll"))

@bp.route("/")
def read():
    articles= Articles.query.all()
    logging.info(articles)

    if articles is not None:
        return(render_template("article/read.html", articles=articles, cols_page=1))

@bp.route("/read/<id>")
def article_view(id):
    matrices_processed = []

    article = Articles.query.filter_by(id=id).first()
    order = ""

    if not article is None:
        for state in article.stateOrder:
            order += str(state.id) + ","
        session["current"] = 0
        session["name"] = article.name

    session["order"] = order[:-1]
    splitOrder = session["order"].split(",")
    print("session order")
    print(session["order"])
    state_first = Articles.query.filter_by(id=splitOrder[0]).first()

    #logger.info(matrices_processed)
    return redirect(url_for("state.read", id=state_first.id, cols_page=1))

