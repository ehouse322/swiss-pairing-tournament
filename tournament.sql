-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

\c postgres;
DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;
\c tournament;

CREATE TABLE players(
id serial PRIMARY KEY,
names text
);

CREATE TABLE matches(
id serial references players(id),
wins int,
losses int,
match_total int,
match_points int);

--INSERT INTO players (names)
--VALUES ('Evan'), ('James'), ('Eric'), ('Philip');

--INSERT INTO matches (wins, losses, match_total, match_points)
--VALUES (3, 1, 4, 9), (1, 3, 4, 3), (2, 2, 4, 6), (2, 2, 4, 6);


