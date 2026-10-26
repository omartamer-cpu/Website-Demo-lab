USE company;

-- Insert departments before employees.
INSERT INTO DEPARTMENT
    (Dnumber, Dname, mgr_ssn, mgr_start_date)
VALUES
    (1, 'IT', NULL, NULL),
    (2, 'HR', NULL, NULL),
    (3, 'Finance', NULL, NULL);

-- Insert employees into existing departments.
INSERT INTO EMPLOYEE
    (ssn, fname, lname, bdate, address, gender, salary, Dno)
VALUES
    ('111111111', 'Omar', 'Tamer',
     '2004-05-10', 'Alexandria', 'M', 15000.00, 1),

    ('222222222', 'Sara', 'Ahmed',
     '2000-03-15', 'Cairo', 'F', 12000.00, 2),

    ('333333333', 'Ali', 'Hassan',
     '1998-11-20', 'Alexandria', 'M', 18000.00, 3);

-- Assign managers after the employees exist.
UPDATE DEPARTMENT
SET mgr_ssn = '111111111', mgr_start_date = '2026-01-01'
WHERE Dnumber = 1;

UPDATE DEPARTMENT
SET mgr_ssn = '222222222', mgr_start_date = '2026-02-01'
WHERE Dnumber = 2;

UPDATE DEPARTMENT
SET mgr_ssn = '333333333', mgr_start_date = '2026-03-01'
WHERE Dnumber = 3;

-- Insert projects into existing departments.
INSERT INTO PROJECT (Pnumber, Pname, Plocation, Dno)
VALUES
    (101, 'Website', 'Alexandria', 1),
    (102, 'Recruitment', 'Cairo', 2),
    (103, 'Budget System', 'Alexandria', 3);

-- Display the results.
SELECT * FROM DEPARTMENT;
SELECT * FROM EMPLOYEE;
SELECT * FROM PROJECT;