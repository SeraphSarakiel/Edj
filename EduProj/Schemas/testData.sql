INSERT INTO matrices (rows, cols, data)
VALUES (3, 3, "1,2,3,4,5,6,7,8,9");

INSERT INTO matrices (rows, cols, data)
VALUES (4,4,"1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1");

INSERT INTO graphs (max_x, min_x, max_y, min_y, grad, coeffizienten)
VALUES (7,0,7,0,2,3);

INSERT INTO graphs (max_x, min_x, max_y, min_y, grad, coeffizienten)
VALUES (7,3,7,2,5,2);

INSERT INTO articles (name, stateOrder) 
VALUES ("Test1", "1,3,2");

INSERT INTO articles (name, stateOrder)
VALUES ("Test2", "1,2,3");

INSERT INTO states (name,comment,matrixId,articleId)
VALUES ("Test1", "This is test1", 1,1);

INSERT INTO states (name,comment,graphId, articleId)
VALUES ("Test2", "This is test2", 1,2);

INSERT INTO states (name,comment,graphId,matrixId, articleId)
VALUES ("Test3", "This is test3", 2,2,3);