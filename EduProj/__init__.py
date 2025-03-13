import os

from flask import Flask

def create_app(test_config=None):
    # create and cofigure the app
    app = Flask(__name__, instance_relative_config=True, template_folder="templates") #config fiels relative to instance folder
    app.config.from_mapping( 
        SECRET_KEY='dev', 
        DATABASE=os.path.join(app.instance_path, 'EduProj.sqlite'),
    )

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

    

    import EduProj.db as db
    db.init_app(app)
    
    import EduProj.matrix as matrix 
    app.register_blueprint(matrix.bp)

    import EduProj.state as state
    app.register_blueprint(state.bp)
    
    import EduProj.article as article
    app.register_blueprint(article.bp)

    import EduProj.graph as graph
    app.register_blueprint(graph.bp)

    return app