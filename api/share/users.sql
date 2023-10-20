-- users.sql

PRAGMA foreign_keys=ON;
BEGIN TRANSACTION;

-- Create the Users table
DROP TABLE IF EXISTS Users;
CREATE TABLE IF NOT EXISTS Users (
    CWID INTEGER PRIMARY KEY,
    
    Name TEXT NOT NULL,
    Middle TEXT NULL,
    LastName TEXT NOT NULL,

    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    
    Role TEXT NOT NULL CHECK (role IN ('instructor', 'registrar', 'student'))
);

-- pre populate database 
-- chatGPT was used to generate some of the data
-- Users Table
INSERT INTO Users (CWID, Name, Middle, LastName, username, password, Role) VALUES
    -- 1 Registrar
    (1, 'John', NULL, 'Doe', 'registrar1', 'registrarpass1', 'registrar'),

    -- 10 Instructors
    (2, 'Alice', 'M.', 'Smith', 'instructor1', 'instructorpass1', 'instructor'),
    (3, 'Bob', 'J.', 'Johnson', 'instructor2', 'instructorpass2', 'instructor'),
    (4, 'Carol', 'A.', 'Wilson', 'instructor3', 'instructorpass3', 'instructor'),
    (5, 'David', 'B.', 'Clark', 'instructor4', 'instructorpass4', 'instructor'),
    (6, 'Eve', 'C.', 'Martin', 'instructor5', 'instructorpass5', 'instructor'),
    (7, 'Frank', 'D.', 'Brown', 'instructor6', 'instructorpass6', 'instructor'),
    (8, 'Grace', 'E.', 'Taylor', 'instructor7', 'instructorpass7', 'instructor'),
    (9, 'Henry', 'F.', 'Adams', 'instructor8', 'instructorpass8', 'instructor'),
    (10, 'Ivy', 'G.', 'Anderson', 'instructor9', 'instructorpass9', 'instructor'),
    (11, 'Jack', 'H.', 'Wright', 'instructor10', 'instructorpass10', 'instructor'),

    -- 30 Students
    (12, 'Emma', 'L.', 'Harris', 'student1', 'studentpass1', 'student'),
    (13, 'Oliver', 'N.', 'Lewis', 'student2', 'studentpass2', 'student'),
    (14, 'Sophia', 'O.', 'Young', 'student3', 'studentpass3', 'student'),
    (15, 'Liam', 'P.', 'Brown', 'student4', 'studentpass4', 'student'),
    (16, 'Ava', 'Q.', 'Clark', 'student5', 'studentpass5', 'student'),
    (17, 'Noah', 'R.', 'King', 'student6', 'studentpass6', 'student'),
    (18, 'Isabella', 'S.', 'Hill', 'student7', 'studentpass7', 'student'),
    (19, 'Lucas', 'T.', 'Ward', 'student8', 'studentpass8', 'student'),
    (20, 'Mia', 'U.', 'Turner', 'student9', 'studentpass9', 'student'),
    (21, 'William', 'V.', 'Parker', 'student10', 'studentpass10', 'student'),
    (22, 'Olivia', 'W.', 'Cooper', 'student11', 'studentpass11', 'student'),
    (23, 'Ethan', 'X.', 'Carter', 'student12', 'studentpass12', 'student'),
    (24, 'Charlotte', 'Y.', 'Walker', 'student13', 'studentpass13', 'student'),
    (25, 'Liam', 'Z.', 'Hall', 'student14', 'studentpass14', 'student'),
    (26, 'Ava', 'M.', 'Miller', 'student15', 'studentpass15', 'student'),
    (27, 'Noah', 'N.', 'Hayes', 'student16', 'studentpass16', 'student'),
    (28, 'Isabella', 'O.', 'Baker', 'student17', 'studentpass17', 'student'),
    (29, 'Lucas', 'P.', 'Wright', 'student18', 'studentpass18', 'student'),
    (30, 'Mia', 'Q.', 'Green', 'student19', 'studentpass19', 'student'),
    (31, 'William', 'R.', 'Scott', 'student20', 'studentpass20', 'student'),
    (32, 'Olivia', 'S.', 'Collins', 'student21', 'studentpass21', 'student'),
    (33, 'Ethan', 'T.', 'Bennett', 'student22', 'studentpass22', 'student'),
    (34, 'Charlotte', 'U.', 'Adams', 'student23', 'studentpass23', 'student'),
    (35, 'Liam', 'V.', 'Ward', 'student24', 'studentpass24', 'student'),
    (36, 'Ava', 'W.', 'Turner', 'student25', 'studentpass25', 'student'),
    (37, 'Noah', 'X.', 'Parker', 'student26', 'studentpass26', 'student'),
    (38, 'Isabella', 'Y.', 'Cooper', 'student27', 'studentpass27', 'student'),
    (39, 'Lucas', 'Z.', 'Carter', 'student28', 'studentpass28', 'student'),
    (40, 'Mia', 'A.', 'Walker', 'student29', 'studentpass29', 'student'),
    (41, 'William', 'B.', 'Hall', 'student30', 'studentpass30', 'student');

COMMIT;