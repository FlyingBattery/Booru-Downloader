import threading
import time
import sqlite3
con = sqlite3.connect('./../data/search.db')
cur = con.cursor()
cur.execute("SELECT * FROM search")

rows = cur.fetchall()

for row in rows:
    print(row)
    
cur.execute("SELECT * FROM search WHERE tag LIKE '%digimon%'")

rows = cur.fetchall()

for row in rows:
    print(row)
con.close()