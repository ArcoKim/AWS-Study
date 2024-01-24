# PostgreSQL
## Install
### Amazon Linux 2023
``` bash
sudo dnf update -y
sudo dnf install -y postgresql15
```
### Amazon Linux 2
``` bash
sudo amazon-linux-extras install -y postgresql14
```
## Connect
Please note that you need to set the ENDPOINT_URL, USER_NAME(postgres), and DB_NAME variables.
``` bash
psql --host=$ENDPOINT_URL --port=5432 --username=$USER_NAME --password --dbname=$DB_NAME
```
## Database Example
``` sql
CREATE DATABASE demo with owner postgres;
\l+
\c demo;
```
## Schema Example
``` sql
CREATE SCHEMA wsi authorization postgres;
set search_path to wsi;
\dn+
```
## Table Example
``` sql
CREATE TABLE public.member (
	idx SERIAL NOT NULL AUTO_INCREMENT,
	user_id VARCHAR(20) NOT NULL,
	password VARCHAR(20) NOT NULL,
	PRIMARY KEY(idx)
);
\dt
```
## CRUD Example
``` sql
INSERT INTO public.member(user_id, password) VALUES ('admin', 'pw1234');
SELECT * FROM public.member;
UPDATE public.member SET password = 'pw5678' WHERE user_id = 'admin';
DELETE FROM public.member WHERE user_id = 'admin';
```