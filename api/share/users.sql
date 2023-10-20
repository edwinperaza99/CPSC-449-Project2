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
INSERT INTO Users (CWID, username, password, Role) VALUES
    -- 1 Registrar
    (1, 'registrar1', 'registrarpass1', 'registrar'),

    -- 10 Instructors
    (2, 'instructor1', 'instructorpass1', 'instructor'),
    (3, 'instructor2', 'instructorpass2', 'instructor'),
    (4, 'instructor3', 'instructorpass3', 'instructor'),
    (5, 'instructor4', 'instructorpass4', 'instructor'),
    (6, 'instructor5', 'instructorpass5', 'instructor'),
    (7, 'instructor6', 'instructorpass6', 'instructor'),
    (8, 'instructor7', 'instructorpass7', 'instructor'),
    (9, 'instructor8', 'instructorpass8', 'instructor'),
    (10, 'instructor9', 'instructorpass9', 'instructor'),
    (11, 'instructor10', 'instructorpass10', 'instructor'),

    -- 30 Students
    (12, 'student1', 'studentpass1', 'student'),
    (13, 'student2', 'studentpass2', 'student'),
    (14, 'student3', 'studentpass3', 'student'),
    (15, 'student4', 'studentpass4', 'student'),
    (16, 'student5', 'studentpass5', 'student'),
    (17, 'student6', 'studentpass6', 'student'),
    (18, 'student7', 'studentpass7', 'student'),
    (19, 'student8', 'studentpass8', 'student'),
    (20, 'student9', 'studentpass9', 'student'),
    (21, 'student10', 'studentpass10', 'student'),
    (22, 'student11', 'studentpass11', 'student'),
    (23, 'student12', 'studentpass12', 'student'),
    (24, 'student13', 'studentpass13', 'student'),
    (25, 'student14', 'studentpass14', 'student'),
    (26, 'student15', 'studentpass15', 'student'),
    (27, 'student16', 'studentpass16', 'student'),
    (28, 'student17', 'studentpass17', 'student'),
    (29, 'student18', 'studentpass18', 'student'),
    (30, 'student19', 'studentpass19', 'student'),
    (31, 'student20', 'studentpass20', 'student'),
    (32, 'student21', 'studentpass21', 'student'),
    (33, 'student22', 'studentpass22', 'student'),
    (34, 'student23', 'studentpass23', 'student'),
    (35, 'student24', 'studentpass24', 'student'),
    (36, 'student25', 'studentpass25', 'student'),
    (37, 'student26', 'studentpass26', 'student'),
    (38, 'student27', 'studentpass27', 'student'),
    (39, 'student28', 'studentpass28', 'student'),
    (40, 'student29', 'studentpass29', 'student'),
    (41, 'student30', 'studentpass30', 'student');

COMMIT;