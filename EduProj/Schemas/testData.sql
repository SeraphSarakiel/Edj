INSERT INTO matrices (rows, cols, data)
VALUES (3, 3, "1,2,3,4,5,6,7,8,9");

INSERT INTO matrices (rows, cols, data)
VALUES (4,4,"1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1");

INSERT INTO graphs (max_x, min_x, max_y, min_y, grad, coeffizienten)
VALUES (5,-5,5,-5,1,"1,0");

INSERT INTO graphs (max_x, min_x, max_y, min_y, grad, coeffizienten)
VALUES (10,0,10,0,2,"1,0,0");

INSERT INTO articles (name, stateOrder) 
VALUES ("Test1", "1,3,2");

INSERT INTO articles (name, stateOrder)
VALUES ("Test2", "1,2,3");

INSERT INTO comment (comment,stateId) 
VALUES ("This is test1", 1)

INSERT INTO comment (comment, stateId)
VALUES ("This is test2", 2)

INSERT INTO comment (comment, stateId)
VALUES ("This is test3", 3)


INSERT INTO states (name,comment,matrixId,articleId, col_state)
VALUES ("Test1", "1",1, 1);

INSERT INTO states (name,comment, matrixId,articleId,col_state)
VALUES ("Test2", "1,2",2, 2);

INSERT INTO states (name,comment,graphId,matrixId, articleId, col_state)
VALUES ("Test3", 2,"2,2,1",3,3);
