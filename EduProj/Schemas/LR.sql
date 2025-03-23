INSERT INTO matrices (rows, cols, data)
VALUES (4, 4, "1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1");

INSERT INTO matrices (rows, cols, data)
VALUES (4,4,"2,4,3,5,-4,-7,-5,-8,6,8,2,2,9,4,9,-2,14");

INSERT INTO matrices (rows, cols, data)
VALUES (4, 4, "1,0,0,0,-2,1,0,0,3,0,1,0,2,0,0,1");

INSERT INTO matrices (rows, cols, data)
VALUES (4,4,"2,4,3,5,0,1,1,2,0,-4,-7,-6,0,1,-8,4");

INSERT INTO matrices (rows, cols, data)
VALUES (4, 4, "1,0,0,0,-2,1,0,0,3,-4,1,0,2,1,0,1");

INSERT INTO matrices (rows, cols, data)
VALUES (4,4,"2,4,3,5,0,1,1,2,0,0,-3,2,0,0,-9,2");

INSERT INTO matrices (rows, cols, data)
VALUES (4, 4, "1,0,0,0,-2,1,0,0,3,-4,1,0,2,1,3,1");

INSERT INTO matrices (rows, cols, data)
VALUES (4,4,"2,4,3,5,0,1,1,2,0,0,-3,2,0,0,0,-4");




INSERT INTO states (name,matrixId,articleId, col_state)
VALUES ("LR Step 1", "1,2",1, 2);

INSERT INTO comments (comment, stateId) 
VALUES ("This is the initial State for L Matrix", 1);

INSERT INTO comments (comment, stateId)
VALUES ("This is the initial State for R Matrix", 1);

INSERT INTO states (name,matrixId,articleId, col_state)
VALUES ("LR Step 2",  "3,4",1, 2);

INSERT INTO comments (comment, stateId) 
VALUES ("II - (-2)I; III-3I; IV-2I", 2);

INSERT INTO comments (comment, stateId) 
VALUES ("II - (-2)I; III-3I; IV-2I", 2);

INSERT INTO states (name,matrixId,articleId, col_state)
VALUES ("LR Step 3", "5,6",1, 2);

INSERT INTO comments (comment, stateId) 
VALUES ("III-(-4)I; IV-1I", 3);

INSERT INTO comments (comment, stateId) 
VALUES ("III-(-4)I;IV-1I", 3);


INSERT INTO states (name,matrixId,articleId, col_state)
VALUES ("LR Step 3", "7,8",1, 2);

INSERT INTO comments (comment, stateId) 
VALUES ("This is the final state for L Matrix", 4);

INSERT INTO comments (comment, stateId) 
VALUES ("This is the final state for R Matrix", 4);

INSERT INTO articles (name, stateOrder) 
VALUES ("LR Zerlegung", "1,2,3,4");


