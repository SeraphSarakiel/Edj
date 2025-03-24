import importlib.util

initspec = importlib.util.spec_from_file_location("__init__","./EduProj/__init__.py")
dbspec = importlib.util.spec_from_file_location("db","./EduProj/db.py")

init = importlib.util.module_from_spec(initspec)
db = importlib.util.module_from_spec(dbspec)

initspec.loader.exec_module(init)
dbspec.loader.exec_module(db)

import pytest
import os



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
    client.post("/state/create", data={"name":"testState",
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
    


