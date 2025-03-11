import importlib.util

initspec = importlib.util.spec_from_file_location("__init__","../__init__.py")
dbspec = importlib.util.spec_from_file_location("db","../db.py")

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
def init_db(app):
    db.init_db()

@pytest.fixture
def init_testdata(init_db):
    db.populate_testdata()     

def test_setup(app,init_db,init_testdata):
    assert True==False;
