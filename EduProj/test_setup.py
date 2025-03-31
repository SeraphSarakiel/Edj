import importlib.util

initspec = importlib.util.spec_from_file_location("__init__","./EduProj/__init__.py")
dbspec = importlib.util.spec_from_file_location("db","./EduProj/db.py")

init = importlib.util.module_from_spec(initspec)
db = importlib.util.module_from_spec(dbspec)

initspec.loader.exec_module(init)
dbspec.loader.exec_module(db)

import pytest
import os

from EduProj.GraphGenerators import BasicGraph


@pytest.fixture
def app():
    app = init.create_app()
    app.config.update({
        "TESTING": True,
        "SECRET_KEY": "dev",
        "DATABASE": os.path.join(app.instance_path, "EduProjTest.sqlite")
    })


    
    #other setup

    yield app

    #cleanup

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture
def app_context(app):
    with app.app_context():
        yield

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture
def init_db(app, app_context, runner):
    result = runner.invoke(args="init-db")

@pytest.fixture
def init_testdata(init_db, runner):
    result = runner.invoke(args="populate-testdata")     

@pytest.fixture
def client(app):
    return app.test_client()

def test_setup(app,client,init_db,init_testdata):
    assert True == True


def test_state_creation(app,client, app_context, init_db): 
    test_db = db.get_db()
    client.post("templates/state/create", data={"name":"testState",
                                                 "comment1":"testComment",
                                                 "comment2":"testComment2",
                                                 "matrix_id": "1,2",
                                                 "col_state": "2"})
    actual_row = test_db.execute("SELECT * FROM states "
                                 "WHERE name = 'testState'").fetchone()
    actual_comments = test_db.execute("SELECT * FROM comments "
    "WHERE stateId = ?", (actual_row.data["id"],)).fetchall()

    assert actual_row.data["name"] == "testState"
    assert actual_row.data["matrix_id"] == "1,2"
    assert actual_row.data["col_state"] == 2
    assert actual_comments[0] == "testComment"
    assert actual_comments[1] == "testComment2"


def test_create_graph(app,client, app_context, init_db):
    test_db = db.get_db()
    client.post("templates/graph/create", data={"max_x" : "10",
                                       "min_x" : "-10",
                                       "max_y" : "10",
                                       "min_y" : "-10",
                                       "grad" : "1",
                                       "coeffizienten" : "2,0"})
    actual_graph = test_db.execute("SELECT * FROM graphs "
                                   "WHERE id = 2").fetchone()
    assert actual_graph["max_x"] == 10
    assert actual_graph["min_x"] == -10
    assert actual_graph["max_y"] == 10
    assert actual_graph["min_y"] == -10
    assert actual_graph["grad"] == 1
    assert actual_graph["coeffizienten"] == "2,0"

#can't find read
def test_read_graph(app,client, app_context, init_db):   
    response = client.get("templates/graph/read/3")
    test_db = db.get_db()
    actual_graph = test_db.execute("SELECT * FROM graphs "
                                   "WHERE id = 2").fetchone()
    graphGenerator = BasicGraph.BasicGraph(actual_graph)
    graphProcessed = graphGenerator.generate()
    
    assert str.encode(graphProcessed) in response.data
    
#also doesn't do the update
def test_update_graph(app,client, app_context, init_db):
    test_db = db.get_db()
    client.post("templates/graph/update/2", data = {"max_x" : "20",
                                        "min_x" : "-20",
                                        "max_y" : "20",
                                        "min_y" : "-20",
                                        "grad" : "2",
                                        "coeffizienten" : "1,0,0"})
    
    actual_graph = test_db.execute("SELECT * FROM graphs "
                                   "WHERE id = 2").fetchone()
    
    assert actual_graph["max_x"] == 20
    assert actual_graph["min_x"] == -20
    assert actual_graph["max_y"] == 20
    assert actual_graph["min_y"] == -20
    assert actual_graph["grad"] == 2
    assert actual_graph["coeffizienten"] == "1,0,0"
    
#not implemented yet
def test_delete_graph(app,client, app_context, init_db):
    assert True