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

INSERT INTO events (Name, Location, Description, Year) Values 
('Something', 'University of Mary Washington', 'stuff stuff and more stuff', '2016-3-12'),
('Something Else', 'University of Mary Washington again', 'stuff stuff and more stuff', '2016-3-12');

--
-- Table structure for table people
--

DROP TABLE IF EXISTS people
CREATE TABLE people (
    ID serial NOT NULL,
    Name varchar(50) NOT NULL default '',
    Birth date,
    Death date,
    Description varchar(400) NOT NULL default '',
    PRIMARY KEY (ID)
);

INSERT INTO people (Name, Birth, Death, Description) Values
('George Washington','1732-2-22','1799-12-14','stuff stuff and more stuff'),
('Robin Williams','1951-7-21','2014-8-11','stuff stuff and more stuff');

--
-- Table structure for table users
--

DROP TABLE IF EXISTS users
CREATE TABLE users (
    ID serial NOT NULL,
    Username varchar(20) NOT NULL,
    Email varchar(60) NOT NULL,
    Firstname varchar(35),
    Lastname varchar(35),
    Company varchar(80),
    Address varchar(70),
    City varchar(40),
    State varchar(40),
    Country varchar(40),
    PostalCode varchar(10),
    Phone varchar(24),
    Fax varchar(24),
    PRIMARY KEY (ID)
);