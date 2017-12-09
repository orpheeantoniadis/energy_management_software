DROP DATABASE IF EXISTS sdi_ems;
CREATE DATABASE sdi_ems;
\c sdi_ems

DROP TABLE IF EXISTS pi CASCADE;
DROP TABLE IF EXISTS sensors CASCADE;
DROP TABLE IF EXISTS measures CASCADE;
DROP TABLE IF EXISTS drivers CASCADE;

CREATE TABLE drivers(
  id int,
  type varchar,
  value int,
  last_modif timestamp,
  CONSTRAINT key_drivers PRIMARY KEY (id,type)
);

CREATE TABLE sensors(
  id int,
  controller varchar,
  location varchar,
  CONSTRAINT key_sensors PRIMARY KEY (id,controller)
);

CREATE TABLE pi(
  ip varchar(15) PRIMARY KEY,
  port int,
  name varchar
);

-- maybe create a function which check if id & controller exists before adding mesures
CREATE TABLE measures(
  id int,
  controller varchar,
  humidity int CHECK (humidity BETWEEN 1 AND 100) DEFAULT NULL,
  luminance int DEFAULT NULL,
  temperature int DEFAULT NULL,
  battery int DEFAULT NULL,
  date timestamp,
  motion boolean DEFAULT NULL,
  CONSTRAINT key_measures PRIMARY KEY (id,controller,date)
);
