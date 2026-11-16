USE company;

INSERT INTO department (Dnumber, Dname, mgr_ssn, mgr_start_date) VALUES
(1,'HR',NULL,NULL),(2,'IT',NULL,NULL),(3,'Sales',NULL,NULL),(4,'Marketing',NULL,NULL); -- Marketing has no employees

-- Ahmed has no supervisor; supervisors are inserted before their employees
INSERT INTO employee VALUES
('111111111','Ahmed','Hassan','1980-03-12','Alexandria','M',6500,NULL,1),
('222222222','Sara','Ali','1988-07-21','Cairo','F',5200,'111111111',2),
('333333333','Omar','Khaled','1990-01-05','Alexandria','M',4500,'222222222',2),
('444444444','Mona','Samir','1992-11-30','Giza','F',3800,'222222222',2),
('555555555','Youssef','Nabil','1995-05-17','Alexandria','M',2800,'111111111',3),
('666666666','Laila','Farid','1993-09-09','Cairo','F',2900,'111111111',1);

UPDATE department SET mgr_ssn='111111111', mgr_start_date='2015-01-01' WHERE Dnumber=1;
UPDATE department SET mgr_ssn='222222222', mgr_start_date='2018-06-01' WHERE Dnumber=2;
UPDATE department SET mgr_ssn='555555555', mgr_start_date='2021-03-15' WHERE Dnumber=3;

INSERT INTO project VALUES
(1,'Website','Alexandria',2),(2,'Mobile App','Cairo',2),
(3,'Recruitment','Alexandria',1),(4,'Ad Campaign','Giza',4); -- nobody works on project 4

INSERT INTO works_on VALUES
('222222222',1,12),('222222222',2,10),  -- Sara works on two projects
('333333333',1,15),('333333333',2,9),
('444444444',2,8),('111111111',3,6),
('666666666',3,14),('555555555',1,5);

INSERT INTO dependent VALUES
('222222222','Adam','M','2015-05-01','Son'),
('222222222','Nour','F','2018-02-14','Daughter'),
('111111111','Huda','F','1982-08-20','Spouse');
