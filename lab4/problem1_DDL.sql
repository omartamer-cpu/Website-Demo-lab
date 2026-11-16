DROP DATABASE IF EXISTS company;
CREATE DATABASE company;
USE company;

CREATE TABLE department (
  Dnumber        INT PRIMARY KEY,
  Dname          VARCHAR(30) NOT NULL UNIQUE,
  mgr_ssn        CHAR(9) NULL,
  mgr_start_date DATE
) ENGINE=InnoDB;

CREATE TABLE employee (
  ssn       CHAR(9) PRIMARY KEY,
  fname     VARCHAR(30) NOT NULL,
  lname     VARCHAR(30) NOT NULL,
  bdate     DATE,
  address   VARCHAR(60),
  gender    CHAR(1),
  salary    DECIMAL(10,2),
  super_ssn CHAR(9) NULL,
  Dno       INT NOT NULL,
  FOREIGN KEY (super_ssn) REFERENCES employee(ssn),
  FOREIGN KEY (Dno) REFERENCES department(Dnumber)
) ENGINE=InnoDB;

-- department <-> employee reference each other, so this FK is added afterwards
ALTER TABLE department
  ADD FOREIGN KEY (mgr_ssn) REFERENCES employee(ssn);

CREATE TABLE project (
  Pnumber   INT PRIMARY KEY,
  Pname     VARCHAR(30) NOT NULL,
  Plocation VARCHAR(30),
  Dno       INT NOT NULL,
  FOREIGN KEY (Dno) REFERENCES department(Dnumber)
) ENGINE=InnoDB;

CREATE TABLE works_on (
  essn  CHAR(9),
  Pno   INT,
  hours DECIMAL(4,1),
  PRIMARY KEY (essn, Pno),
  FOREIGN KEY (essn) REFERENCES employee(ssn),
  FOREIGN KEY (Pno)  REFERENCES project(Pnumber)
) ENGINE=InnoDB;

CREATE TABLE dependent (
  essn           CHAR(9),
  dependent_name VARCHAR(30),
  gender         CHAR(1),
  bdate          DATE,
  relationship   VARCHAR(20),
  PRIMARY KEY (essn, dependent_name),
  FOREIGN KEY (essn) REFERENCES employee(ssn)
) ENGINE=InnoDB;
