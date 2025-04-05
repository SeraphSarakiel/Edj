"""from flask import (
    Blueprint, flash, render_template, request, jsonify, abort, redirect, url_for
)

from werkzeug.security import generate_password_hash, check_password_hash

from EduProj.db import get_db

from .models import User

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=["GET","POST"])
def login():
    
        
    return render_template('auth/login.html')
 
@bp.route('/signup', methods=["GET","POST"])
def signup():
    if request.method == "POST":
        username  = request.form["username"]
        password = request.form["password"]
        
        user = User.query.filter_by(username=username).first()
        
        if user:
            flash("Username already in use")
            return redirect(url_for("auth.signup"))
        
        new_user = User(username = username, password = generate_password_hash(password, method="sha256"))
        db = get_db()
        db.session.add(new_user)
        db.session.commit()
    
    return render_template('auth/signup.html')

@bp.route('/logout')
def logout():
    return 'Logout'"""