import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, make_response
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
    return [[float(data[i+j*3]) for i in range(rows)] for j in range(cols)]

bp = Blueprint('article', __name__)

@bp.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        name = request.form["name"]
        order = request.form["order"]
        

        db = get_db()
        error = None

        if not name or not order:
            error = "All Values need to be filled"

        if error is None:
            try:
                db.execute(
                    "INSERT INTO articles (name, stateOrder) "
                    "VALUES (?, ?)",
                    (name, order)
                )
                db.commit()
                flash("created")
            except db.IntegrityError:
                error = f"article already exists"
        else:
            return redirect(url_for("article.display"))
        
        flash(error)
        
    return render_template("article/create.html")

@bp.route("/")
def read():
    db = get_db()
    articles = db.execute(
        "SELECT * FROM articles"
    ).fetchall()

    if articles is not None:
        return(render_template("article/read.html", articles=articles))

@bp.route("/read/<id>")
def article_view(id):
    db = get_db()
    matrices_processed = []


    article = db.execute(
        "SELECT * FROM articles WHERE id = ?",
        (id,)
    ).fetchone()

    if not article is None:
        session["order"] = article["stateOrder"]
        session["current"] = 0
        session["name"] = article["name"]

    splitOrder = session["order"].split(",")
            
    state_first = db.execute(
        "SELECT * FROM states WHERE id = ?",
        (splitOrder[0],)
    ).fetchone()

    logger.info(matrices_processed)
    return redirect(url_for("state.read", id=state_first["id"]))

