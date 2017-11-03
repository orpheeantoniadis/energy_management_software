DROP DATABASE IF EXISTS sdi_ems;
CREATE DATABASE sdi_ems;
\c sdi_ems

DROP TABLE IF EXISTS pi CASCADE;
DROP TABLE IF EXISTS sensors CASCADE;
DROP TABLE IF EXISTS mesures CASCADE;


CREATE TABLE sensors(
  id int,
  controller varchar,
  location varchar,
  CONSTRAINT key_sensors PRIMARY KEY (id,controller)
);

CREATE TABLE pi(
  ip varchar(15) PRIMARY KEY,
  port int,
  controller varchar
);

-- maybe create a function which check if id & controller exists before adding mesures
CREATE TABLE mesures(
  id int,
  controller varchar,
  humidity int CHECK (humidity BETWEEN 1 AND 100) DEFAULT NULL,
  luminence int DEFAULT NULL,
  temperature int DEFAULT NULL,
  battery int DEFAULT NULL,
  datte timestamp,
  motion boolean DEFAULT NULL,
  CONSTRAINT key_mesures PRIMARY KEY (id,controller,datte)
);
