# biodata-form
Group 3 VUA-SEN 305 Biodata Form Web Assignment

Installations 
pip install Flask
pip install mysql-connector-python

SQL CODE FOR CREATING THE TABLES

**Code
CREATE DATABASE student_biodata;

USE student_biodata;

CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    dob DATE NOT NULL,
    gender VARCHAR(20) NOT NULL,
    state VARCHAR(100),
    nationality VARCHAR(100),
    email VARCHAR(150) NOT NULL,
    phone VARCHAR(30) NOT NULL,
    address TEXT,
    matric VARCHAR(50) NOT NULL UNIQUE,
    level VARCHAR(10) NOT NULL,
    faculty VARCHAR(100) NOT NULL,
    department VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
**Paste this in SQL in your local host before running the code 

Configure python method
def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="student_biodata")

to your local database credentials

To run the code =" python app.py"