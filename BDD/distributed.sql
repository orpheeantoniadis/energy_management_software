DROP DATABASE IF EXISTS distributedserver;

DROP TABLE IF EXISTS pi CASCADE;
DROP TABLE IF EXISTS sensors CASCADE;
DROP TABLE IF EXISTS battery CASCADE;
DROP TABLE IF EXISTS humidity CASCADE;
DROP TABLE IF EXISTS luminence CASCADE;
DROP TABLE IF EXISTS temperature CASCADE;
DROP TABLE IF EXISTS motion CASCADE;


CREATE TABLE pi(
  ip varchar(15) PRIMARY KEY,
  port int,
  name varchar
);

CREATE TABLE sensors(
  id int PRIMARY KEY,
  controller varchar,
  location varchar,
);

CREATE TABLE battery(
  id int PRIMARY KEY,
  battery int CHECK (battery BETWEEN 1 AND 100),
);
