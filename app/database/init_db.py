import sqlite3

conn = sqlite3.connect('app/users.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS games (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    white_player1 TEXT NOT NULL,
    white_player2 TEXT NOT NULL,
    black_player1 TEXT NOT NULL,
    black_player2 TEXT NOT NULL,
    result TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS moves (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    game_id INTEGER NOT NULL,
    from_pos TEXT NOT NULL,
    to_pos TEXT NOT NULL,
    piece TEXT NOT NULL,
    FOREIGN KEY (game_id) REFERENCES games (id)
)
''')

conn.commit()
conn.close()
print("Banco de dados criado.")

