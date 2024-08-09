CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY,
  username TEXT,
  password TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  balance INTEGER
);

CREATE TABLE IF NOT EXISTS sessions (
  token TEXT PRIMARY KEY,
  user_id INTEGER,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES user (id)
);

CREATE TABLE IF NOT EXISTS games (
  id INTEGER PRIMARY KEY,
  name TEXT,
  games_played INTEGER,
  total_value INTEGER
);

CREATE TABLE IF NOT EXISTS history (
  id INTEGER PRIMARY KEY,
  user_id INTEGER,
  value INTEGER,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  game_id INTEGER,
  field_1 REAL,
  field_2 TEXT,
  FOREIGN KEY (game_id) REFERENCES games (id),
  FOREIGN KEY (user_id) REFERENCES user (id)
);

INSERT INTO games (name, games_played, total_value) VALUES ("coinflip", 0, 0);
INSERT INTO games (name, games_played, total_value) VALUES ("blackjack", 0, 0);
INSERT INTO games (name, games_played, total_value) VALUES ("roulette", 0, 0);
INSERT INTO games (name, games_played, total_value) VALUES ("minesweeper", 0, 0);