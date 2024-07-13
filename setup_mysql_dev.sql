-- prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS sat_track_db;
CREATE USER IF NOT EXISTS 'sat_track'@'localhost' IDENTIFIED BY 'sat_track_pwd';
GRANT ALL PRIVILEGES ON `sat_track_db`.* TO 'sat_track'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'sat_track'@'localhost';
FLUSH PRIVILEGES;
