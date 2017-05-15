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

CREATE TABLE players (
  id  serial PRIMARY KEY,
  name text NOT NULL,
  record integer DEFAULT 0
);

CREATE TABLE matches (
  id serial PRIMARY KEY,
  match_id integer NOT NULL,
  player_id integer REFERENCES players (id),
  result integer CHECK (result = 0 OR result = 1),
  round_num integer NOT NULL
);
