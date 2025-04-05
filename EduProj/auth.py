from flask import (
    Blueprint, flash, render_template, request, jsonify, abort, redirect, url_for
)

from flask_login import login_user

from werkzeug.security import generate_password_hash, check_password_hash

from . import db

from .models import User

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=["GET","POST"])
def login():
    if request.method == "POST":
        username  = request.form["username"]
        password = request.form["password"]
        
        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login'))
        flash("logged in")
    
       
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
        
        new_user = User(username = username, password = generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
    
    return render_template('auth/signup.html')

@bp.route('/logout')
def logout():
    return 'Logout'