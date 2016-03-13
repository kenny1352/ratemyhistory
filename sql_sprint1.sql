DROP DATABASE IF EXISTS world;
CREATE DATABASE  ratemyhistory;
\c ratemyhistory;



--
-- Table structure for table events
--

DROP TABLE IF EXISTS events;
CREATE TABLE events (
  ID serial NOT NULL,
  Name varchar(35)  NOT NULL default '',
  Location varchar(35) NOT NULL default '',
  Description varchar(400) NOT NULL default '',
  year date,
  PRIMARY KEY  (ID)
) ;