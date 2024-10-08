# MySQL
## Install
### Amazon Linux 2023
``` bash
sudo dnf update -y
sudo dnf install -y mariadb105
```
### Amazon Linux 2
``` bash
sudo yum install -y mariadb
```
## Connect
Please note that you need to set the ENDPOINT_URL and USER_NAME(admin) variables.
``` bash
mysql -h $ENDPOINT_URL -P 3306 -u $USER_NAME -p
```
## Database Example
``` sql
CREATE DATABASE demo;
USE demo;
```
## Table Example
``` sql
CREATE TABLE member (
	idx INT NOT NULL AUTO_INCREMENT,
	user_id VARCHAR(20) NOT NULL,
	password VARCHAR(20) NOT NULL,
	PRIMARY KEY(idx)
);

CREATE TABLE employees (
	emp_no		INT				NOT NULL,
	birth_date	DATE 			NOT NULL,
	first_name	VARCHAR(14)		NOT NULL,
	last_name	VARCHAR(16)		NOT NULL,
	gender		ENUM('M','F')	NOT NULL,
	hire_date	DATE			NOT NULL,
	PRIMARY KEY (emp_no)
);
```
## CRUD Example
``` sql
INSERT INTO member(user_id, password) VALUES ('admin', 'pw1234');
source insert.sql;
SELECT * FROM member;
UPDATE member SET password = 'pw5678' WHERE user_id = 'admin';
DELETE FROM member WHERE user_id = 'admin';
```
## Index Example
``` sql
CREATE INDEX name ON employees (first_name, last_name);
```
## New User
``` sql
CREATE USER 'admin'@'%' IDENTIFIED BY 'Mysql1234!';
GRANT ALL PRIVILEGES ON *.* TO 'admin'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;
```