\i distributed_create.sql

-- file used only for testes !

insert into drivers values(1,'radiator',20,'2004-10-19 10:23:54');
insert into drivers values(1,'store',70,'2004-10-19 10:23:54');
insert into drivers values(2,'radiator',90,'2004-10-19 10:23:54');
insert into drivers values(2,'store',250,'2004-10-19 10:23:54');
insert into drivers values(10,'radiator',40,'2004-10-19 10:23:54');

insert into rules values(1,'A501',20,'2004-10-19 10:23:54');
insert into rules values(2,'A501',20,'2004-10-19 10:23:54');
insert into rules values(3,'A501',80,'2004-10-19 10:23:54');
insert into rules values(4,'A501',80,'2004-10-19 10:23:54');

  -- update measures set temperature=2 where battery=0 and id=2 and controller like 'Pi 1' and humidity=25 and luminance=25;
-- update measures set temperature=25,motion=false where battery=0 and id=2 and controller like 'Pi 1' and humidity=25 and luminance=25;
-- SELECT * FROM measures m JOIN sensors s ON (m.id = s.id AND m.controller = s.controller) WHERE location ILIKE 'A501' ORDER BY date DESC LIMIT 1;

insert into sensors values(1,'Pi lab1','Room 401');
insert into sensors values(1,'Pi lab2','Room 502');
insert into sensors values(2,'Pi lab1','Room 405');
insert into sensors values(2,'Pi lab2','Room 502');
insert into sensors values(3,'Pi lab2','Room 503');

insert into pi values('129.194.184.124',5000,'Pi lab1');
insert into pi values('129.194.184.125',5000,'Pi lab2');

--                     id, control, humid, lum, temp, batt, date, motion
insert into measures values(1,'Pi lab1',20,520,18,80,'2004-10-19 10:23:54',false);
insert into measures values(1,'Pi lab1',21,520,5,100,'2004-10-19 10:27:54',true);
insert into measures values(1,'Pi lab2',1,300,25,10,'2004-10-19 10:23:54',false);
insert into measures values(2,'Pi lab1',50,800,18,21,'2004-10-19 10:23:54',true);
insert into measures values(2,'Pi lab2',82,250,30,30,'2004-10-19 10:23:54',true);
insert into measures values(3,'Pi lab2',12,222,10,80,'2004-10-19 10:23:54',false);
insert into measures values(1,'Pi lab1',2,333,17,90,'2004-10-19 10:31:54',false);
