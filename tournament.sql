-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;

CREATE TABLE players ( -- stores info on players in tournament
  id  serial PRIMARY KEY,
  name text NOT NULL -- name of the player
);

CREATE TABLE matches ( -- stores the per match info for the tournament
  match_id serial PRIMARY KEY, -- unique to each player per match
  winner_id integer REFERENCES players (id), -- player id from players table
  loser_id integer REFERENCES players (id) -- same
);
