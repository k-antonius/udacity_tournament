#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def cursQuery(curs, queryString, tup = None):
    '''Connet to database, make a query, return the cursor.
    @param queryString: the sql query as a string.
    @return: cursor object at the query location
    '''
    curs.execute(queryString, tup)
    return curs

def makeQuery(queryString):
    '''
    Makes a query and returns the result.
    @param queryString: the SQL query as a string.
    @return: list of tuples containing the cells of the table  
    '''
    conn = connect()
    curs = cursQuery(conn.cursor(), queryString)
    try:
        return curs.fetchall()
    except (psycopg2.ProgrammingError):
        conn.commit()
    conn.close()

def insertRows(queryString, tup):
    '''
    Insert rows into the forum database.
    '''
    conn = connect()
    cursQuery(conn.cursor(), queryString, tup)
    conn.commit()
    conn.close()

def deleteMatches():
    """Remove all the match records from the database."""
    query = "DELETE FROM matches *;"
    makeQuery(query)


def deletePlayers():
    """Remove all the player records from the database."""
    query = "DELETE FROM players *;"
    makeQuery(query)


def countPlayers():
    """Returns the number of players currently registered."""
    query = "SELECT COUNT(id) FROM players;"
    
    result = makeQuery(query)
    print result
    return result[0][0]


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    query = "INSERT INTO players (name) VALUES (%s);"
    insertRows(query, (name,))


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    query = """select players.*, count(player_id) as num_matches 
            from players join matches on players.id = matches.player_id 
            group by players.id;"""
    return makeQuery(query)


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """


