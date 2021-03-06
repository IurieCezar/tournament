#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament

import psycopg2
import bleach

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    cur = conn.cursor()
    QUERY = "DELETE FROM each_match;"
    cur.execute(QUERY)
    conn.commit()
    conn.close()

def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    cur = conn.cursor()
    QUERY = "DELETE FROM players;"
    cur.execute(QUERY)
    conn.commit()
    conn.close()

def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    cur = conn.cursor()
    QUERY = "SELECT count(*) FROM players;"
    cur.execute(QUERY)
    num_players = cur.fetchone()[0]
    conn.close()
    return num_players

def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    name = bleach.clean(name)
    conn = connect()
    cur = conn.cursor()
    QUERY = "INSERT INTO players (name) VALUES (%s);"
    cur.execute(QUERY, (name,))
    conn.commit()
    conn.close()


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
    conn = connect()
    cur = conn.cursor()
    QUERY = "SELECT * FROM player_standings;"
    cur.execute(QUERY)
    player_stand = cur.fetchall()
    conn.close()
    return player_stand


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    winner, loser = bleach.clean(winner), bleach.clean(loser)
    conn = connect()
    cur = conn.cursor()
    QUERY = "INSERT INTO each_match (winner_id, loser_id) VALUES (%s, %s);"
    cur.execute(QUERY, (winner, loser))
    conn.commit()
    conn.close()

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
    conn = connect()
    cur = conn.cursor()
    QUERY = "SELECT id, name FROM player_standings;"
    cur.execute(QUERY)
    players = cur.fetchall()
    conn.close()
    index = 0
    pairings=[]
    while index < countPlayers()/2:
        pairing = players.pop()+players.pop()
        pairings.append(pairing)
        index = index+1
    return pairings


