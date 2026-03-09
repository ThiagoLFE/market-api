import sqlite3

def get_connection():
    return sqlite3.connect("market.db", check_same_thread=False)

def create_tables():
    db = get_connection()
    db.execute("""
    CREATE TABLE IF NOT EXISTS product(id integer PRIMARY KEY AUTOINCREMENT, name text NOT NULL, price float, stock integer, image text DEFAULT NULL)
""")
    db.commit()
    db.close()