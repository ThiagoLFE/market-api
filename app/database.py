import sqlite3

def database():
    con = sqlite3.connect("market.db")
    cur = con.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS product(id integer, name text, price float, stock integer)")
    
    # testing if datable already exists 
    res = cur.execute("SELECT name FROM sqlite_master")
    if res.fetchone() is None:
        raise Exception("Any table is found")

    # adding data to table
    cur.execute("""
    INSERT INTO product VALUES
        (1, 'Borracha', 3.20, 20),
        (2, 'Martalo', 12.75, 15)
""")
    # saving changes

    con.commit()

    res = cur.execute("""
    SELECT * FROM product
""")
    print(res.fetchall())
    return con
database()