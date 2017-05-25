#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#
''' Functions that perform operations on a postgresSQL database to implement
a swiss style tournament system.
@author: Kenneth LaMantia
'''

import psycopg2

#database name
DATABASE = "tournament"

def connect():
    '''Connect to the PostgreSQL database.  Returns a database connection.
    If the connection fails, this will throw an exception.
    '''
    try:
        return psycopg2.connect("dbname=" + DATABASE)
    except psycopg2.OperationalError:
        print ("A connection error ocurred. Check that the database exists" +
        " or simply try again.")

def cursQuery(curs, queryString, tup=None):
    '''Connet to database, make a query, return the cursor.
    @param curs: a psycopg2 cursor
    @param queryString: the sql query as a string.
    @param tup: tuple used to pass arguments where query needs to be formatted
    @return: cursor object at the query location
    '''

    curs.execute(queryString, tup)
    return curs


def staticQuery(queryString, tup):
    '''Makes a query and returns the result.
    @param queryString: the sql query as a string.
    @param tup: tuple used to pass arguments where query needs to be formatted
    @return: list of tuples containing the cells of the table
    '''

    conn = connect()
    curs = cursQuery(conn.cursor(), queryString, tup)
    result = curs.fetchall()
    conn.close()
    return result

def mutatingQuery(queryString, tup):
    '''Insert rows into the forum database safely.
    @param queryString: the sql query as a string.
    @param tup: tuple used to pass arguments where query needs to be formatted
    '''
    conn = connect()
    cursQuery(conn.cursor(), queryString, tup)
    conn.commit()
    conn.close()


def deleteMatches():
    '''Remove all the match records from the database.
    '''

    query = "DELETE FROM matches *"
    mutatingQuery(query, (None,))

def deletePlayers():
    '''Remove all the player records from the database.
    '''

    query = "DELETE FROM players *"
    mutatingQuery(query, (None,))


def countPlayers():
    '''Returns the number of players currently registered.
    '''

    query = "SELECT COUNT(id) FROM players"

    result = staticQuery(query, (None,))
    print result
    return result[0][0]


def registerPlayer(name):
    '''Adds a player to the tournament database.
    @param name: name of a player in the tournament
    '''

    query = "INSERT INTO players (name) VALUES (%s)"
    mutatingQuery(query, (name,))


def playerStandings():
    '''Returns a list of the players and their win records, sorted by wins
    in descending order.
    @return:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    '''

    query = """WITH n_wins AS 
    (SELECT players.id AS id, COUNT(matches.winner_id) 
     AS num_wins FROM players LEFT OUTER JOIN matches ON
     players.id = matches.winner_id GROUP BY players.id), n_matches AS
    (SELECT players.id AS id, COUNT(CASE WHEN id = matches.loser_id 
                              or id = matches.winner_id 
                              then 1 else null end)
      AS num_matches
      FROM players LEFT OUTER JOIN matches
      ON (id = matches.loser_id OR id = matches.winner_id)
      GROUP BY id)
    SELECT players.*, n_wins.num_wins, n_matches.num_matches
    FROM players, n_wins, n_matches WHERE players.id = n_wins.id AND
    players.id = n_matches.id ORDER BY players.name
    """
    return staticQuery(query, (None,))


def reportMatch(winner, loser):
    '''Records the outcome of a single match between two players, updating
    the tables in the database as needed.
      @param winner:  the id number of the player who won
      @param loser:  the id number of the player who lost
    '''
    query = "INSERT INTO matches (winner_id, loser_id) VALUES (%s, %s)"
    mutatingQuery(query, (winner, loser))

def swissPairings():
    '''Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    @return:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    '''

    query = """SELECT id, name FROM (
    (SELECT players.id AS id, players.name, COUNT(matches.winner_id) 
    AS num_wins
    FROM players LEFT OUTER JOIN matches ON
    players.id = matches.winner_id
    GROUP BY players.id ORDER BY num_wins DESC)) AS wins"""
    result = staticQuery(query, (None,))
    print result

    def foldl(fun, acc, items):
        '''Like classic fold/reduce but process two list items
        at a time, not one.
        @param fun: list processing function, takes a two element list
        @param acc: list accumulator
        @param items: list to process
        '''

        if len(items) == 0:
            return acc
        else:
            return foldl(fun, fun(items[:2], acc), items[2:])

    return foldl(lambda x, y: y + [(x[0][0], x[0][1], x[1][0], x[1][1])],
                 list(), result)
