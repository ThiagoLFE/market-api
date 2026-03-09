import sqlite3

def get_connection():
    return sqlite3.connect("market.db", check_same_thread=False)

def create_tables():
    db = get_connection()
    db.execute("""
        CREATE TABLE IF NOT EXISTS product(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, price float, stock INTEGER, image TEXT DEFAULT NULL)
    """)
    db.execute("""
        CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, email TEXT UNIQUE NOT NULL, hash_password TEXT NOT NULL, is_admin BOOLEAN NOT NULL DEFAULT 0)
    """)
    db.commit()
    db.close()