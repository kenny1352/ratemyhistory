\c postgres;
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
    Location varchar(50) NOT NULL default '',
    Description varchar(500) NOT NULL default '',
    Year date,
    Rating integer,
    Views integer NOT NULL default 0,
    PRIMARY KEY  (ID)
) ;

INSERT INTO events (Name, Location, Description, Year, Views) Values 
('Watergate Break-in', 'Watergate Hotel. Washington, D.C.','Five men connected to Nixon''s reelection campaign broke into the Democratic National Committee Headquarters and were caught by a security guard.', '1972-6-17', 10),
('Ford pardons Nixon', 'White House, Washington D.C.', 'President Gerald Ford pardons Nixon after Nixon resigns from office and Ford takes the presidency. Ford pardons Nixon ''for all crimes he ''committed or may have committed'' while in office''. ', '1974-9-8', 15),
('Boston Tea Party', 'Boston, Massachusetts', 'Defying the Tea Act, the Sons of Liberty disguised as Native Americans poured an entire shipment of tea into the Boston Harbor.','1773-12-16', 82),
('Battle of Waterloo', 'Waterloo, Netherlands (present-day Belgium)', 'Napolean Bonaparte was defeated and ended his reign as Emperor of the French.', '1815-7-18', 3),
('The Jungle', 'N/A', 'A book written by socialist Upton Sinclair and published in 1904. It promoted the idea of socialism. Readers only retained the disgusting allegations about the meatpacking industrys'' practices. Led to the passage of The Pure Food and Drugs Act of 1906 and the Federal Meat Inspection Act.', '1905-2-25', 5),
('Triangle Shirtwaist Fire', 'New York City, New York', 'A fire in the Triangle Shirtwaist Company 10-story factory building that killed 145 workers. Demonstrated the horrible labor conditions and fire regulations in the early twentieth century. Although the Triangle Shirtwaist Factory Company owners were not indicted on manslaughter charges from their workers'' deaths, it led to the passage of the Sullivan-Hoey Fire Prevention Law in October of 1911 and other reforms.', '1911-3-25', 19),
('Flying Machine', 'Kitty Hawk, North Carolina', 'The first successfule powered airplane invented by Wilbur and Orville Wright.', '1903-12-17', 34),
('Apollo 11', 'Moon', 'First American flight into space and landing of humans on the Moon under President John F. Kennedy''s administration. Astronauts Neil Armstrong, Edwin "Buzz" Aldrin stepped on the Moon.', '1969-7-20', 67);


--
-- Table structure for table people
--

DROP TABLE IF EXISTS people;
CREATE TABLE people (
    ID serial NOT NULL,
    Name varchar(50) NOT NULL default '',
    Birth date,
    Death date,
    Description varchar(500) NOT NULL default '',
    Rating integer,
    Views integer NOT NULL default 0,
    PRIMARY KEY (ID)
);

INSERT INTO people (Name, Birth, Death, Description, Views) Values
('Elizabeth I', '1533-9-7', '1603-3-24', 'Queen of England for 45 years and last Tudor monarch.', 10),
('Christopher Columbus', '1451-9-26', '1506-5-20', 'Italian explorer who reached the New World in 1492. Established a permanent contact of the Old World to the New World.', 82),
('Benito Mussolini', '1883-7-29', '1945-4-28', 'A Facist dictator in Italy during World War II. Created the Facist Party in Italy and was its leader from 1922 to 1943. Allied with Nazi Germany and Japan during World War II.', 23),
('Theodore Roosevelt', '1858-10-27', '1919-1-6', 'Served as the 26th President of the United States from 1901 to 1909. Avid reader, author, historian, naturalist, explorer, and soldier. With the assasination of Present William McKinley, Theodore Roosevelt became the youngest man in history at the age of 42, to become president. Passed the Pure Food and Drugs Act of 1906 and Federal Meat Inspection Act of 1906 after reading The Jungle by Upton Sinclair.', 32),
('Wilbur Wright', '1867-4-16', '1912-5-30', 'Wilbur and his brother, Orville were the inventors and builders of the first airplane.', 14),
('Orville Wright', '1871-8-19', '1948-1-30', 'Orville and his brother, Wilbur were the inventors and builders of the first airplane.', 15),
('Upton Sinclair', '1878-9-20', '1968-11-25', 'A socialist and author of the notable muckraker novel, The Jungle. Exposed the working conditions and the meat packing industries'' practices during the early twentieth century. Readers only focused on the horrible conditions that directly impacted them. The purpose of the novel was to promote socialism.', 48), 
('John F. Kennedy', '1917-5-29', '1963-11-22', '35th President of the United States of America and was assassinated on November 22, 1963. Under his presidency was the Cuban Missile Crisis, Bay of Pigs Invasion, establishment of the Peace Corps, Civil Rights Movement, construction of the Berlin Wall, beginning of the Space Race including space flight of Apollo 11.', 1917),
('Neil Armstrong', '1930-8-5', '2012-8-25', 'American astronaut and person to walk on the Moon from the Apollo 11 mission along with Edwin "Buzz" Aldrin.', 1), 
('Edwin "Buzz" Aldrin', '1930-1-20', NULL, 'American astronaut and person to walk on the Moon from the Apollo 11 mission along with Neil Armstrong.', 0),
('Rosa Parks', '1913-2-4', '2005-10-24', 'Civil Rights activist who refused to give up her seat on a bus to a white passenger in Montgomery, Alabama. Prompted the Montgomery boycott and other events to end racial segregation int he United States.', 0),
('Martin Luther King, Jr.', '1929-1-15', '1968-4-4', 'Baptist minister and Civil Rights activist who started the Movement in the mid-1950s in the United States. Spoke the infamous "I Have a Dream" speech on the steps of the Washington Monument in Washington, D.C. on August 28, 1963. Talked with E.D. Nixon and other NAACP leaders about Rosa Parks and her arrest and organized a citywide bus boycott. John F. Kennedy phone called Coretta Scott King when Martin Luther King, Jr. was in jail. Was assassinated by James Earl Ray on April 4, 1968.', 0);

--
-- Table structure for table users
--

DROP TABLE IF EXISTS users;
CREATE TABLE users (
    userID serial NOT NULL,
    Username varchar(20) NOT NULL,
    Email varchar(60) NOT NULL,
    Password text NOT NULL,
    PRIMARY KEY (userID)
);

INSERT INTO users (Username, Email, Password) VALUES
('test','test@test.com', crypt('test', gen_salt('bf'))),
('admin', 'admin@admin.com', crypt('admin', gen_salt('bf')));


DROP TABLE IF EXISTS chat;
CREATE TABLE IF NOT EXISTS chat (
  chat_id SERIAL NOT NULL,
  message text NOT NULL,
  PRIMARY KEY (chat_id)
);

INSERT INTO chat (message) VALUES
('Welcome to chat');

DROP TABLE IF EXISTS usersChat;
CREATE TABLE IF NOT EXISTS usersChat (
  chat_id SERIAL NOT NULL,
  sender text NOT NULL,
  PRIMARY KEY (chat_id)
);

INSERT INTO usersChat (sender) VALUES
('Admin');
--
-- Table structure for table relations
--

DROP TABLE IF EXISTS eventtoperson;
CREATE TABLE eventtoperson (
    EventID integer NOT NULL,
    PersonID integer NOT NULL,
    PRIMARY KEY (EventID, PersonID),
    FOREIGN KEY (EventID) REFERENCES events(ID),
    FOREIGN KEY (PersonID) REFERENCES people(ID)
);

INSERT INTO eventtoperson (EventID, PersonID) VALUES
(1,1),
(2,1),
(1,2),
(2,2);

GRANT INSERT, UPDATE, SELECT ON ALL TABLES IN SCHEMA public To assist;
GRANT USAGE ON users_userid_seq to assist;
GRANT USAGE ON events_id_seq to assist;
GRANT USAGE ON people_id_seq to assist;
GRANT USAGE ON chat_chat_id_seq to assist;
GRANT USAGE ON userschat_chat_id_seq to assist;
---GRANT USAGE ON relations_id_seq to assist;

