DROP TABLE IF EXISTS pi CASCADE;
DROP TABLE IF EXISTS sensors CASCADE;
DROP TABLE IF EXISTS battery CASCADE;
DROP TABLE IF EXISTS humidity CASCADE;
-- DROP TABLE IF EXISTS luminence CASCADE;
-- DROP TABLE IF EXISTS temperature CASCADE;
-- DROP TABLE IF EXISTS motion CASCADE;

CREATE TABLE sensors(
  id int,
  controller varchar,
  location varchar,
  CONSTRAINT key_sensors PRIMARY KEY (id,controller)
);

CREATE TABLE pi(
  ip varchar(15) PRIMARY KEY,
  port int,
  controller varchar -- faire une fonction qui met tout à jour en cas de changement
);

 CREATE TABLE battery(
  id int,
  controller varchar,
  lvl int CHECK (lvl BETWEEN 1 AND 100),
  CONSTRAINT key_battery PRIMARY KEY (id,controller)
);

CREATE TABLE humidity(
  id int,
  controller varchar,
  value int CHECK (value BETWEEN 1 AND 100),
  datte timestamp,
  CONSTRAINT key_humidty PRIMARY KEY (id,controller,value,datte)
);



-- insert into sensors values(1,'Pi lab1','Room 401');
-- insert into pi values('129.194.184.124',5000,'Pi lab1');
-- insert into battery values(1,'Pi lab1',80);
