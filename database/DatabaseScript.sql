CREATE SCHEMA IF NOT EXISTS VisitorTracking;

USE VisitorTracking;

CREATE TABLE IF NOT EXISTS Address (
    id INT PRIMARY KEY,
    street VARCHAR(255) NOT NULL,
    number VARCHAR(10) NOT NULL,
    postcode VARCHAR(10) NOT NULL,
    city VARCHAR(255) NOT NULL,
    floor INT
);

CREATE TABLE IF NOT EXISTS Company (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address_id INT,
    FOREIGN KEY (address_id) REFERENCES Address(id)
);

CREATE TABLE IF NOT EXISTS Person (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    mail VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(15) UNIQUE NOT NULL,
    address_id INT,
    FOREIGN KEY (address_id) REFERENCES Address(id)
);

CREATE TABLE IF NOT EXISTS Company_Employee (
    id INT PRIMARY KEY,
    company_id INT,
    person_id INT,
    job_title VARCHAR(255),
    started_date DATE,
    FOREIGN KEY (company_id) REFERENCES Company(id),
    FOREIGN KEY (person_id) REFERENCES Person(id)
);

CREATE TABLE IF NOT EXISTS Visit_Purpose (
    id INT PRIMARY KEY,
    reason VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS Visit (
    id INT PRIMARY KEY,
    visitor_id INT,
    employee_id INT,
    company_id INT,
    checked_in DATETIME,
    checked_out DATETIME,
    visit_purpose_id INT,
    FOREIGN KEY (visitor_id) REFERENCES Person(id),
    FOREIGN KEY (employee_id) REFERENCES Company_Employee(id),
    FOREIGN KEY (company_id) REFERENCES Company(id),
    FOREIGN KEY (visit_purpose_id) REFERENCES Visit_Purpose(id)
);
