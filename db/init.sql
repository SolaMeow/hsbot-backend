CREATE DATABASE IF NOT EXISTS mydb;
USE mydb;

CREATE TABLE IF NOT EXISTS Player (
    id INT AUTO_INCREMENT,
    name VARCHAR(255),
    region ENUM('AP', 'US', 'EU'),
    mode ENUM('standard', 'wild'),
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS Ranking (
    player_id INT,
    `rank` INT,
    timestamp DATETIME,
    batch INT,
    FOREIGN KEY (player_id) REFERENCES Player(id)
);