CREATE SCHEMA IF NOT EXISTS VisitorTracking;
USE VisitorTracking;

CREATE TABLE IF NOT EXISTS Address (
    id INT PRIMARY KEY AUTO_INCREMENT,
    street VARCHAR(255) NOT NULL,
    number VARCHAR(10) NOT NULL,
    postcode VARCHAR(10) NOT NULL,
    city VARCHAR(255) NOT NULL,
    floor INT
);

CREATE TABLE IF NOT EXISTS Company (
    id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address_id INT,
    FOREIGN KEY (address_id) REFERENCES Address(id)
);

CREATE TABLE IF NOT EXISTS Employee (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    mail VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(15) UNIQUE NOT NULL,
    address_id INT,
    FOREIGN KEY (address_id) REFERENCES Address(id)
);

CREATE TABLE IF NOT EXISTS Company_Employee (
    id INT PRIMARY KEY AUTO_INCREMENT,
    company_id VARCHAR(20),
    employee_id INT,
    job_title VARCHAR(255),
    started_date DATE,
    FOREIGN KEY (company_id) REFERENCES Company(id),
    FOREIGN KEY (employee_id) REFERENCES Employee(id)
);

CREATE TABLE IF NOT EXISTS Visit_Purpose (
    id INT PRIMARY KEY AUTO_INCREMENT,
    reason VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS Visit (
    id INT PRIMARY KEY AUTO_INCREMENT,
    visitor_phone_nr VARCHAR(15) NOT NULL,
    visitor_name VARCHAR(255) NOT NULL,
    employee_id INT,
    company_id VARCHAR(20),
    checked_in DATETIME,
    checked_out DATETIME,
    visit_purpose_id INT,
    FOREIGN KEY (employee_id) REFERENCES Company_Employee(id),
    FOREIGN KEY (company_id) REFERENCES Company(id),
    FOREIGN KEY (visit_purpose_id) REFERENCES Visit_Purpose(id)
);
