DROP DATABASE IF EXISTS company;
CREATE DATABASE company;
USE company;

CREATE TABLE DEPARTMENT (
    Dnumber INT NOT NULL,
    Dname VARCHAR(50) NOT NULL,
    mgr_ssn CHAR(9),
    mgr_start_date DATE,
    PRIMARY KEY (Dnumber)
);

CREATE TABLE EMPLOYEE (
    ssn CHAR(9) NOT NULL,
    fname VARCHAR(30) NOT NULL,
    lname VARCHAR(30) NOT NULL,
    bdate DATE,
    address VARCHAR(100),
    gender CHAR(1),
    salary DECIMAL(10,2),
    Dno INT NOT NULL,
    PRIMARY KEY (ssn),
    FOREIGN KEY (Dno) REFERENCES DEPARTMENT(Dnumber)
);

ALTER TABLE DEPARTMENT
ADD FOREIGN KEY (mgr_ssn) REFERENCES EMPLOYEE(ssn);

CREATE TABLE PROJECT (
    Pnumber INT NOT NULL,
    Pname VARCHAR(50) NOT NULL,
    Plocation VARCHAR(50),
    Dno INT NOT NULL,
    PRIMARY KEY (Pnumber),
    FOREIGN KEY (Dno) REFERENCES DEPARTMENT(Dnumber)
);