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

CREATE TABLE mesures(
  id int,
  controller varchar,
  humidity int CHECK (humidity BETWEEN 1 AND 100),
  luminence int,
  temperature int,
  battery int,
  datte timestamp,
  motion boolean,
  CONSTRAINT key_mesures PRIMARY KEY (id,controller,datte)
);

insert into sensors values(1,'Pi lab1','Room 401');
insert into sensors values(1,'Pi lab2','Room 502');
insert into sensors values(2,'Pi lab1','Room 405');
insert into sensors values(2,'Pi lab2','Room 502');
insert into sensors values(3,'Pi lab2','Room 503');

insert into pi values('129.194.184.124',5000,'Pi lab1');
insert into pi values('129.194.184.125',5000,'Pi lab2');

--                     id, control, humid, lum, temp, batt, date, motion
insert into mesures values(1,'Pi lab1',20,520,18,80,'2004-10-19 10:23:54',false);
insert into mesures values(1,'Pi lab1',21,520,5,100,'2004-10-19 10:27:54',true);
insert into mesures values(1,'Pi lab2',1,300,25,10,'2004-10-19 10:23:54',false);
insert into mesures values(2,'Pi lab1',50,800,18,21,'2004-10-19 10:23:54',true);
insert into mesures values(2,'Pi lab2',82,250,30,30,'2004-10-19 10:23:54',true);
insert into mesures values(3,'Pi lab2',12,222,10,80,'2004-10-19 10:23:54',false);
insert into mesures values(1,'Pi lab1',2,333,17,90,'2004-10-19 10:31:54',false);
