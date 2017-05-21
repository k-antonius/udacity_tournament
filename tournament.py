#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#
''' Functions that perform operations on a postgresSQL database to implement
a swiss style tournament system.
@author: Kenneth LaMantia
'''

import psycopg2


def connect():
    '''Connect to the PostgreSQL database.  Returns a database connection.
    '''

    return psycopg2.connect("dbname=tournament")


def cursQuery(curs, queryString, tup=None):
    '''Connet to database, make a query, return the cursor.
    @param curs: a psycopg2 cursor
    @param queryString: the sql query as a string.
    @param tup: tuple used to pass arguments where query needs to be formatted
    @return: cursor object at the query location
    '''

    curs.execute(queryString, tup)
    return curs


def makeQuery(queryString, tup=None):
    '''Makes a query and returns the result.
    @param queryString: the sql query as a string.
    @param tup: tuple used to pass arguments where query needs to be formatted
    @return: list of tuples containing the cells of the table
    '''

    conn = connect()
    curs = cursQuery(conn.cursor(), queryString, tup)
    try:
        return curs.fetchall()
    except psycopg2.ProgrammingError:
        conn.commit()
    conn.close()


def insertUpdate(queryString, tup):
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

    query = "DELETE FROM matches *;"
    makeQuery(query)
    resetRecord = "UPDATE players SET record = 0;"
    makeQuery(resetRecord)


def deletePlayers():
    '''Remove all the player records from the database.
    '''

    query = "DELETE FROM players *;"
    makeQuery(query)


def countPlayers():
    '''Returns the number of players currently registered.
    '''

    query = "SELECT COUNT(id) FROM players;"

    result = makeQuery(query)
    print result
    return result[0][0]


def registerPlayer(name):
    '''Adds a player to the tournament database.
    @param name: name of a player in the tournament
    '''

    query = "INSERT INTO players (name) VALUES (%s);"
    insertUpdate(query, (name,))


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

    query = """SELECT players.*, COUNT(player_id) AS num_matches
            FROM players LEFT OUTER JOIN matches ON 
            players.id = matches.player_id 
            GROUP BY players.id ORDER BY players.id;"""
    return makeQuery(query)


def reportMatch(winner, loser):
    '''Records the outcome of a single match between two players, updating
    the tables in the database as needed.
      @param winner:  the id number of the player who won
      @param loser:  the id number of the player who lost
    '''

    def getCurMatch(query):
        '''Gets the current match number
        @param query: sql query string
        '''

        prevMatch = makeQuery(query)[0][0]
        if prevMatch != None:
            return prevMatch + 1
        else:
            return 1

    def getCurRound(query):
        '''Gets the current round.
        @param query: sql query string
        @return: the number of the current round. If this is the first round,
        returns 1.
        '''

        prevRound = makeQuery(query)[0][0]
        if prevRound != None:
            roundCount = makeQuery("""SELECT COUNT(round_num) FROM matches
                 WHERE round_num = %s """, (prevRound,))[0][0]
            if roundCount < countPlayers():
                return prevRound
            else:
                return prevRound + 1
        else:
            return 1

    curRound = getCurRound("""SELECT MAX(round_num) FROM matches""")
    curMatch = getCurMatch("""SELECT MAX(match_id) FROM matches""")
    insert = """INSERT INTO matches (match_id, player_id, result, round_num)
             VALUES (%s, %s, %s, %s), (%s, %s, %s, %s)"""
    content = (curMatch, winner, 1, curRound,
               curMatch, loser, 0, curRound)
    insertUpdate(insert, content)
    # need to update players table for wins
    updatePlayers = """UPDATE players SET record = record + 1
                    WHERE id = %s"""
    insertUpdate(updatePlayers, (winner,))


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

    query = """SELECT id, name FROM players ORDER BY record DESC"""
    result = makeQuery(query, (None,))
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
