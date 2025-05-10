from flask import current_app, g
import click
from werkzeug.security import generate_password_hash

from EduProj import db
from EduProj.models import User, Matrices, Articles, States, Graphs, Comments

tables = [User, Matrices, Articles, States, Graphs, Comments]

@click.command('init-db')
def init_db():
    with current_app.app_context():
        for table in tables:
            db.metadata.drop_all(bind=db.engine,tables=[table.__table__])
            #db.session.query(table).delete()
            #db.session.commit()
            

@click.command('populate-testdata')
def populate_testdata():
    with current_app.app_context():
        user1 = User(username="test", password=generate_password_hash("test"))
        db.session.add(user1)
        
        matrix1 = Matrices(rows=3, cols=3, data="1,2,3,4,5,6,7,8,9") #, stateId = [1]
        matrix2 = Matrices(rows=4,cols=4,data="1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1") #stateId = [2]
        db.session.add(matrix1)
        db.session.add(matrix2)
        
        article1 = Articles(name="Test1")
        article2 = Articles(name="Test2")
        db.session.add(article1)
        db.session.add(article2)
        
        state1 = States(name="Test1", col_state=1) #, matrixId=[1] 
        state1.matrixId = [matrix1]
        state1.order = "M"
 
        state2 = States(name="Test2", col_state=2) #matrixId=[1,2]
        state2.matrixId = [matrix1, matrix2]
        state2.order = "M,M"

        state3= States(name="Test3",  col_state=3) # matrixId=[2,2,1], graphId=[2],
        state3.matrixId = [matrix2, matrix2, matrix1]
        state3.order = "M,G,M,M"
        
        db.session.add(state1)
        db.session.add(state2)
        db.session.add(state3)

        article1.stateOrder = [state1, state3, state2]
        article2.stateOrder = [state1, state2, state3]
        
        graph1 = Graphs(max_x=5, min_x=-5, max_y=5, min_y=-5, grad=1, coeffizienten="1,0")
        graph2 = Graphs(max_x=10, min_x=0, max_y=10, min_y=0, grad=2, coeffizienten="1,0,0")
        state3.graphId = [graph2]
        db.session.add(graph1)
        db.session.add(graph2)
        
        comment1 = Comments(comment="This is test1", stateId=1)
        comment2 = Comments(comment="This is test2", stateId=2)
        comment3 = Comments(comment="This is test2", stateId=3)
        db.session.add(comment1)
        db.session.add(comment2)
        db.session.add(comment3)
        
        db.session.commit()
    


@click.command('LR')
def LR_seeding():
    with current_app.app_context():
        matrixList = []
        matrixList.append(Matrices(rows=4, cols=4, data="1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1"))
        matrixList.append(Matrices(rows=4, cols=4, data="2,4,3,5,-4,-7,-5,-8,6,8,2,2,9,4,9,-2,14"))
        matrixList.append(Matrices(rows=4, cols=4, data="1,0,0,0,-2,1,0,0,3,0,1,0,2,0,0,1"))
        matrixList.append(Matrices(rows=4, cols=4, data="2,4,3,5,0,1,1,2,0,-4,-7,-6,0,1,-8,4"))
        matrixList.append(Matrices(rows=4, cols=4, data="1,0,0,0,-2,1,0,0,3,-4,1,0,2,1,0,1"))
        matrixList.append(Matrices(rows=4, cols=4, data="2,4,3,5,0,1,1,2,0,0,-3,2,0,0,-9,2"))
        matrixList.append(Matrices(rows=4, cols=4, data="1,0,0,0,-2,1,0,0,3,-4,1,0,2,1,3,1"))
        matrixList.append(Matrices(rows=4, cols=4, data="2,4,3,5,0,1,1,2,0,0,-3,2,0,0,0,-4"))
        
        for matrix in matrixList:
            db.session.add(matrix)
        
        stateList = []
        stateList.append(States(name="LR Step 1", matrixId="1,2", articleId=1, col_state=2))
        stateList.append(States(name="LR Step 2", matrixId="3,4", articleId=1, col_state=2))
        stateList.append(States(name="LR Step 3", matrixId="5,6", articleId=1, col_state=2))
        
        for state in stateList:
            db.session.add(state)
        
        commentList = []
        commentList.append(Comments(comment="This is the initial State for L Matrix", stateId=1))
        commentList.append(Comments(comment="This is the initial State for R Matrix", stateId=1))
        commentList.append(Comments(comment="II - (-2)I; III-3I; IV-2I", stateId=2))
        commentList.append(Comments(comment="II - (-2)I; III-3I; IV-2I", stateId=2))
        commentList.append(Comments(comment="III-(-4)I; IV-1I", stateId=3))
        commentList.append(Comments(comment="III-(-4)I;IV-1I", stateId=3))
        
        for comment in commentList:
            db.session.add(comment)
            
        db.session.commit()
    