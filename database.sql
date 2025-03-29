-- SQL script to create admin, students, attendance tables
CREATE DATABASE attendance_db;
USE attendance_db;

CREATE TABLE admin (
  id INT PRIMARY KEY AUTO_INCREMENT,
  username VARCHAR(50) NOT NULL,
  password VARCHAR(50) NOT NULL
);

INSERT INTO admin (username, password) VALUES ('admin', 'admin123');

CREATE TABLE students (
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(100),
  photo LONGBLOB
);

CREATE TABLE attendance (
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(100),
  date_time DATETIME
);
CREATE TABLE attendance_reports (
    report_id INT AUTO_INCREMENT PRIMARY KEY,
    report_type VARCHAR(50) NOT NULL,
    total_attendees INT NOT NULL,
    total_absences INT NOT NULL,
    average_attendance DECIMAL(5,2) NOT NULL,
    week1_statistics DECIMAL(5,2) NOT NULL,
    week2_statistics DECIMAL(5,2) NOT NULL,
    week3_statistics DECIMAL(5,2) NOT NULL,
    week4_statistics DECIMAL(5,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);