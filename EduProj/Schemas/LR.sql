INSERT INTO matrices (rows, cols, data)
VALUES (4, 4, "1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1");

INSERT INTO matrices (rows, cols, data)
VALUES (4,4,"2,4,3,5,-4,-7,-5,-8,6,8,2,2,9,4,9,-2,14");

INSERT INTO matrices (rows, cols, data)
VALUES (4, 4, "1,0,0,0,-2,1,0,0,3,0,1,0,2,0,0,1");

INSERT INTO matrices (rows, cols, data)
VALUES (4,4,"2,3,4,5,0,1,1,2,0,-4,-7,-6,0,1,-8,4");


INSERT INTO states (name,comment,matrixId,articleId, col_state)
VALUES ("LR Step 1", "This is the initial state", "1,2",1, 2);


INSERT INTO states (name,comment,matrixId,articleId, col_state)
VALUES ("LR Step 2", "II - (-2)I; III-3I; IV-2I", "3,4",1, 2);

INSERT INTO articles (name, stateOrder) 
VALUES ("LR Zerlegung", "1,2");


