from helper_functions.mysqlClass import MySQL


def get_history_stats(user_id):
    stats = {}
    games = {}
    # get data from db
    with MySQL("SELECT") as curs:
        curs.execute("SELECT (game_id, value) FROM history WHERE user_id = %s", (user_id,))
        history_rows = curs.fetchall()
    with MySQL("SELECT") as curs:
        curs.execute('SELECT (id, game_name) FROM games')

        for row in curs.fetchall():
            games[row[0]] = row[1]
            stats[row[1]] = {
                'games_played': 0,
                'value': 0
            }

    # insert data into stats dict
    for row in history_rows:
        stats[games[row[0]]]['games_played'] += 1
        stats[games[row[0]]]['value'] += row[1]

    # remove games that have not been played yet
    for stat in stats:
        if stat['games_played'] == 0:
            del stats[stat]

    return stats
