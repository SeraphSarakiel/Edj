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

def test_db_make_dicts(app, app_context, init_db, init_testdata):
    test_db = db.get_db()
    cursor = test_db.cursor()
    test_db.execute(
                    "INSERT INTO articles (name, stateOrder) "
                    "VALUES ('test', '1,2,3')"
                )
    test_db.commit()
    row = cursor.execute("SELECT * FROM articles").fetchmany()
    
    result_func = db.make_dicts(cursor, row)
    result_exp = {"id" : 1, "name":"test", "stateOrder":"1,2,3"}
    


    print("descr")
    print(result_func)
    
    assert result_func == result_exp

