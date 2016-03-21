DROP DATABASE IF EXISTS ratemyhistory;
CREATE DATABASE  ratemyhistory;
DROP USER IF EXISTS assist;
CREATE USER assist WITH PASSWORD 'assist';
GRANT ALL PRIVILEGES ON DATABASE ratemyhistory to assist;
\c ratemyhistory;

DROP EXTENSION IF EXISTS pgcrypto;
CREATE EXTENSION pgcrypto;

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
('Something Else', 'University of Mary Washington again', 'stuff stuff and more stuff', '2016-3-12'),
('Watergate Break-in', 'Watergate Hotel. Washington, D.C.','Five men connected to Nixon''s reelection campaign broke into the Democratic National Committee Headquarters and were caught by a security guard.', ' 1972-6-17'),
('Ford pardons Nixon', 'White House, Washington D.C.', 'President Gerald Ford pardons Nixon after Nixon resigns from office and Ford takes the presidency. Ford pardons Nixon ''for all crimes he ''committed or may have committed'' while in office''. ', '1974-9-8');



--
-- Table structure for table people
--

DROP TABLE IF EXISTS people;
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
('Robin Williams','1951-7-21','2014-8-11','stuff stuff and more stuff'),
('Upton Sinclair', '1878-9-20', '1968-11-25', 'Author of The Jungle');
--
-- Table structure for table users
--

DROP TABLE IF EXISTS users;
CREATE TABLE users (
    ID serial NOT NULL,
    Username varchar(20) NOT NULL,
    Email varchar(60) NOT NULL,
    Password text NOT NULL,
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

INSERT INTO users (Username, Email, Password) VALUES
('test','test@test.com', crypt('test', gen_salt('bf'))),
('admin', 'admin@admin.com', crypt('admin', gen_salt('bf')));


-- DROP TABLE IF EXISTS relations
-- CREATE TABLE relations (
    
--     EventID integer NOT NULL,
--     PersonID integer NOT NULL,
--     FOREIGN KEY 
-- );

GRANT INSERT, UPDATE, SELECT ON ALL TABLES IN SCHEMA public To assist;
GRANT USAGE ON users_id_seq to assist;
GRANT USAGE ON events_id_seq to assist;
GRANT USAGE ON people_id_seq to assist;
