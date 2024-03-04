CREATE DATABASE if not exists mining_db;
use mining_db;
DROP TABLE if exists aspersores_data;
CREATE TABLE if not exists aspersores_data (
 `id` int(11) NOT NULL AUTO_INCREMENT,
 `status_aspersores` TEXT DEFAULT NULL,
 `timestamp`  INT DEFAULT NULL,
 `datetime` DATETIME DEFAULT NULL,
 `uploaded` INT NOT NULL DEFAULT 0,
 PRIMARY KEY (`id`)
);
