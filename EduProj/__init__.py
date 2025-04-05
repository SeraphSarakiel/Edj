import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

def create_app(test_config=None):
    # create and cofigure the app
    app = Flask(__name__, instance_relative_config=True, template_folder="templates") #config fiels relative to instance folder
    app.config.from_mapping( 
        SECRET_KEY='dev', 
        SQLALCHEMY_DATABASE_URI='sqlite:///db.sqlite'
    )
    

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    if test_config is None:
        #Load the instance config, if it exists,  when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        #Load the test config if passed in
        app.config.from_mapping(test_config) #used for testing

    #ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route("/entry")
    def entry():
        return "Welcome traveller"

    db.init_app(app)
    
    with app.app_context():
        db.create_all()
    
    import EduProj.matrix as matrix 
    app.register_blueprint(matrix.bp)

    import EduProj.state as state
    app.register_blueprint(state.bp)
    
    import EduProj.article as article
    app.register_blueprint(article.bp)

    import EduProj.graph as graph
    app.register_blueprint(graph.bp)

    return app