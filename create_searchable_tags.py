from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import threading
import json
import time
import os
import sqlite3
import collections

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

## Generates a JSON file that can be used with a search engine.
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

con = sqlite3.connect('.\\data\\images.db')
con.row_factory = dict_factory
cur = con.cursor()

conn = sqlite3.connect('.\\data\\search.db')
conn.row_factory = dict_factory
curr = conn.cursor()

print("Attemping to create table in the tags database.")
curr.execute('CREATE TABLE IF NOT EXISTS tags (tag text, file text)')
conn.commit()

print("Attemping to create table in the tags database.")
curr.execute('CREATE TABLE IF NOT EXISTS search (tag text, file text)')
conn.commit()

print("Truncating data in table in the searchable databse.")
curr.execute('DELETE FROM tags')
conn.commit()

print("Truncating data in table in the searchable databse.")
curr.execute('DELETE FROM search')
conn.commit()

# cur.execute("SELECT * FROM images where `tags` LIKE '%creator:darkmirage%'")
# cur.execute("SELECT * FROM images")
cur.execute("SELECT * FROM images")
rows = cur.fetchall()

search = []
DIR = ".\\data\\images"
numberOfFiles = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))]) + 1
counter = 0
files = []
fileTypes = []
fileBaseNames = []
for file in os.listdir(DIR):
    try:
        fileTypes.append(file.split(".")[1])
        fileBaseNames.append(file.split(".")[0])
        files.append(file)
        # Update Progress Bar
        printProgressBar(counter + 1, numberOfFiles, prefix = 'Progress:', suffix = 'Complete', length = 50)
        counter += 1
    except:
        a=1
print("Loaded {} file names into memory.".format(str(counter)))
fileTypeCollections = dict(collections.Counter(fileTypes))

# for key, value in fileTypeCollections.items():
#    print("File type {} is recorded {} times.". format(key, value))
    
print("Creating searchable database for website.")
numberOfRows = len(rows)
counter = 0
dbTagsInsert = []
dbSearchInsert = []
for row in rows:
    link = row['link']
    direct = row['direct']
    fileName = ""
    filePart = direct.replace('http://xbzszf4a4z46wjac7pgbheizjgvwaf3aydtjxg7vsn3onhlot6sppfad.onion/ipfs/', '')
    '''
    for file in files:
        if file.startswith(filePart):
            fileName = ":3007/images/" + file
            tagsOutput = row['tags'].replace(", ", ",").replace(" ", "_").replace(",", ", ").split(", ")
            for t in tagsOutput:
                search.append({t: fileName})
                curr.execute("INSERT INTO images VALUES (?,?)", (t, fileName))
                conn.commit()
    '''
    if filePart in fileBaseNames:
        file = files[fileBaseNames.index(filePart)]
        fileName = ":3007/images/" + file
        tagsOutput = row['tags'].replace(", ", ",").replace(" ", "_").replace(",", ", ").split(", ")
        dbSearchInsert.append((", ".join(tagsOutput), fileName))
        for t in tagsOutput:
            search.append({t: fileName})
            dbTagsInsert.append((t, fileName))
    # Update Progress Bar
    printProgressBar(counter + 1, numberOfRows, prefix = 'Progress:', suffix = 'Complete', length = 50)
    counter += 1

print("Inserting into tagable database.")
curr.executemany("INSERT INTO tags VALUES (?,?)", dbTagsInsert)
conn.commit()
curr.executemany("INSERT INTO search VALUES (?,?)", dbSearchInsert)
conn.commit()
print("Table updated for tag criteria.")

'''
print("Writing output to JSON file.")
with open('.\\data\\images.json', 'w', encoding='utf-8') as f:
    json.dump(search, f, ensure_ascii=False, indent=4)
print("Complete.")
'''

con.close()
conn.close()