DROP TABLE IF EXISTS matrices;
DROP TABLE IF EXISTS states;
DROP TABLE IF EXISTS articles;
DROP TABLE IF EXISTS graphs;
DROP TABLE IF EXISTS comments;

CREATE TABLE matrices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rows INTEGER,
    cols INTEGER,
    DATA VARCHAR NOT NULL
);

CREATE TABLE articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR NOT NULL,
    stateOrder VARCHAR NOT NULL
);


CREATE TABLE states (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR NOT NULL,
    matrixId VARCHAR,
    graphId INTEGER,
    articleId INTEGER,
    col_state INTEGER,
    FOREIGN KEY(articleId) REFERENCES articles(id),
    FOREIGN KEY(graphId) REFERENCES graphs(id)
);

CREATE TABLE graphs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    max_x INTEGER,
    min_x INTEGER,
    max_y INTEGER,
    min_y INTEGER,
    grad INTEGER,
    coeffizienten VARCHAR
);

CREATE TABLE comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    comment VARCHAR,
    stateId INTEGER, 
    FOREIGN KEY(stateId) REFERENCES state(id)
)





