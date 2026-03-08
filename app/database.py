import sqlite3

def get_connection():
    return sqlite3.connect("market.db")

def create_tables():
    db = get_connection()
    db.execute("""
    CREATE TABLE IF NOT EXISTS product(id integer PRIMARY KEY AUTOINCREMENT, name text NOT NULL, price float, stock integer)
""")
    db.commit()
    db.close()