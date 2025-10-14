import sqlite3, os

DB_PATH = os.path.join(os.path.dirname(__file__), "app.db")

schema = '''
DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    algo TEXT NOT NULL
);
DROP TABLE IF EXISTS products;
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL
);
DROP TABLE IF EXISTS comments;
CREATE TABLE comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author TEXT NOT NULL,
    body TEXT NOT NULL
);
'''
data_products = [
    ("Apple iPhone", 999.0),
    ("Samsung TV", 550.0),
    ("Sony Headphones", 199.9),
]

con = sqlite3.connect(DB_PATH)
cur = con.cursor()
cur.executescript(schema)
cur.executemany("INSERT INTO products(name, price) VALUES (?,?)", data_products)
con.commit()
con.close()
print("Database initialized:", DB_PATH)
