from helper_functions.sqlClass import SQL


def get_history_stats(user_id):
    stats = {}
    games = {}
    # get data from db
    with SQL("SELECT") as curs:
        curs.execute(f'SELECT game_id, value FROM history WHERE user_id = {user_id}')
        history_rows = curs.fetchall()
    with SQL("SELECT") as curs:
        curs.execute('SELECT id, name FROM games')

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
    for stat in list(stats):
        if stats[stat]['games_played'] == 0:
            del stats[stat]

    return stats
