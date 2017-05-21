-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE DATABASE tournament;

DROP TABLE IF EXISTS matches;
DROP TABLE IF EXISTS players;

CREATE TABLE players ( -- stores info on players in tournament
  id  serial PRIMARY KEY,
  name text NOT NULL, -- name of the player
  record integer DEFAULT 0 -- number of wins
);

CREATE TABLE matches ( -- stores the per match info for the tournament
  id serial PRIMARY KEY, -- unique to each player per match
  match_id integer NOT NULL, -- to identify a match
  player_id integer REFERENCES players (id), -- player id from players table
  result integer CHECK (result = 0 OR result = 1), -- 0 for loss 1 for win
  round_num integer NOT NULL -- number of round starting at 1
);
