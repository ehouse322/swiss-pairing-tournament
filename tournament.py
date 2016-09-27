#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    cur = conn.cursor()
    #cur.execute("UPDATE players SET wins = 0, losses = 0, match_total = 0")
    cur.execute("TRUNCATE matches")
    conn.commit()

def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    cur = conn.cursor()
    cur.execute("TRUNCATE players CASCADE")
    conn.commit()

def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT id FROM players")
    player_count = cur.rowcount
    return player_count

def registerPlayer(name_var):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO players (names) VALUES (%s)", (name_var,))
    # cur.execute("INSERT INTO matches (wins, losses, match_total) VALUES (0, 0, 0)")
    conn.commit()

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
    cur.execute("CREATE VIEW myview AS SELECT players.id, players.names, count(matches.winner) as wins FROM players LEFT JOIN matches ON players.id = matches.winner GROUP BY players.id ORDER BY wins desc;")
    cur.execute("CREATE VIEW myview2 AS SELECT players.id, players.names, count(matches.loser) as losses FROM players LEFT JOIN matches ON players.id = matches.loser GROUP BY players.id ORDER BY losses;")
    cur.execute("SELECT myview.id, myview.names, myview.wins, myview2.losses + myview.wins FROM myview JOIN myview2 ON myview.id = myview2.id ORDER BY losses;")
    standings = cur.fetchall()
    return standings

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.
    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO matches (winner, loser) VALUES (%s, %s)", (winner, loser,))
    #cur.execute("UPDATE players SET losses = losses + 1, match_total = match_total + 1 WHERE id = (%s)", (loser,))
    conn.commit()
 
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
    cur.execute("CREATE VIEW myview AS SELECT players.id, players.names, count(matches.winner) as wins FROM players LEFT JOIN matches ON players.id = matches.winner GROUP BY players.id ORDER BY wins desc;")
    cur.execute("CREATE VIEW myview2 AS SELECT players.id, players.names, count(matches.loser) as losses FROM players LEFT JOIN matches ON players.id = matches.loser GROUP BY players.id ORDER BY losses;")
    cur.execute("SELECT players.id, players.names, myview.wins, myview2.losses FROM players JOIN myview ON players.id = myview.id JOIN myview2 ON myview.id = myview2.id ORDER BY myview.wins desc")
    db_info = cur.fetchall()
    player_count = len(db_info)
    swiss_pairs = []
    for i in range(0, player_count , 2):
        swiss_pairs.append((db_info[i][0], db_info[i][1], db_info[i+1][0], db_info[i+1][1]))
    #print(swiss_pairs)
    return swiss_pairs