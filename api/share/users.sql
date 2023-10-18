-- users.sql

PRAGMA foreign_keys=ON;
BEGIN TRANSACTION;

DROP TABLE IF EXIST Users;
CREATE TABLE IF NOT EXISTS Users (
    CWID INTEGER PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    Role TEXT NOT NULL CHECK (role IN ('instructor', 'registrar', 'student'))
);

-- INSERT INTO Users (CWID, email, password, role) VALUES
    

COMMIT;