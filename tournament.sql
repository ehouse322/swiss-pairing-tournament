-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

\c postgres
-- I have been told the above line of code is not necessary, however if I dont use it
-- I cannot drop the tournament database while I am in it.
DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;
\c tournament;

CREATE TABLE players(
	id serial PRIMARY KEY,
	names text
);

CREATE TABLE matches(
	match_id SERIAL PRIMARY KEY,
	winner INTEGER REFERENCES players(id),
	loser INTEGER REFERENCES players(id)
);
