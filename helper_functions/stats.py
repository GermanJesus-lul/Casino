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


def played_game(user_id, balance, game_name, double_field=None, text_field=None):
    # get game_id
    with SQL("SELECT") as curs:
        curs.execute(f'SELECT id FROM games WHERE name="{game_name}"')
        game_id = curs.fetchone()[0]
    # update game stats
    with SQL("UPDATE") as curs:
        curs.execute(f'UPDATE games SET total_value = total_value + {balance}, games_played = games_played + 1 WHERE id={game_id}')
    # add history item
    with SQL("INSERT") as curs:
        if double_field is not None and text_field is not None:
            curs.execute(f'INSERT INTO history (user_id, value, game_id, field_1, field_2)'
                         f' VALUES ({user_id}, {balance}, {game_id}, {double_field}, "{text_field}")')
        elif double_field is not None:
            curs.execute(f'INSERT INTO history (user_id, value, game_id, field_1)'
                         f' VALUES ({user_id}, {balance}, {game_id}, {double_field})')
        elif text_field is not None:
            curs.execute(f'INSERT INTO history (user_id, value, game_id, field_2)'
                         f' VALUES ({user_id}, {balance}, {game_id}, "{text_field}")')
        else:
            curs.execute(f'INSERT INTO history (user_id, value, game_id)'
                         f' VALUES ({user_id}, {balance}, {game_id})')
