DROP DATABASE IF EXISTS ratemyhistory;
CREATE DATABASE  ratemyhistory;
CREATE USER assist WITH PASSWORD 'assist';
GRANT ALL PRIVILEGES ON DATABASE ratemyhistory to assist;
\c ratemyhistory;

--
-- Table structure for table events
--

DROP TABLE IF EXISTS events;
CREATE TABLE events (
  ID serial NOT NULL,
  Name varchar(50)  NOT NULL default '',
  Location varchar(35) NOT NULL default '',
  Description varchar(400) NOT NULL default '',
  Year date,
  PRIMARY KEY  (ID)
) ;

Insert INTO events (Name, Location, Description, Year) Values 
('Something', 'University of Mary Washington', 'stuff stuff and more stuff', '2016-3-12'),
('Something Else', 'University of Mary Washington again', 'stuff stuff and more stuff', '2016-3-12');