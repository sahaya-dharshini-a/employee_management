CREATE DATABASE dc;
USE dc;

CREATE TABLE Users (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    password VARCHAR(50)
);

INSERT INTO Users (username, password) VALUES ('admin', 'admin123');

CREATE TABLE Department (
    DepartmentID INT AUTO_INCREMENT PRIMARY KEY,
    DepartmentName VARCHAR(100) UNIQUE
);

INSERT INTO Department (DepartmentName) VALUES
('HR'), ('IT'), ('Finance'), ('Marketing');

CREATE TABLE Emp (
    EmpID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100),
    Email VARCHAR(100),
    Age INT,
    DepartmentID INT,
    Salary DECIMAL(10,2),
    FOREIGN KEY (DepartmentID) REFERENCES Department(DepartmentID)
);

CREATE TABLE Projects (
    ProjectID INT AUTO_INCREMENT PRIMARY KEY,
    ProjectName VARCHAR(100)
);

INSERT INTO Projects (ProjectName) VALUES
('Website Development'),
('Mobile App'),
('Payroll System');

CREATE TABLE EmployeeProject (
    EmpID INT,
    ProjectID INT,
    PRIMARY KEY (EmpID, ProjectID),
    FOREIGN KEY (EmpID) REFERENCES Emp(EmpID) ON DELETE CASCADE,
    FOREIGN KEY (ProjectID) REFERENCES Projects(ProjectID) ON DELETE CASCADE
);
