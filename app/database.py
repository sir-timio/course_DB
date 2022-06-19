#!/usr/bin/python3

import sqlite3 as sql

conn = sql.connect('../data/data.db')
conn.execute("drop table DOCTOR")


conn.execute('''CREATE TABLE DOCTOR
         (ID INT PRIMARY KEY     NOT NULL,
         NAME           TEXT    NOT NULL,
         AGE            INT     NOT NULL
         );''')

l = [
    (1, "Masha", 22),
    (2, "Sasha", 19),
]
conn.executemany('''insert into DOCTOR values (?, ?, ?)
''', l)

cursor = conn.execute('select id, name, age from DOCTOR')

for row in cursor:
   print(f"ID = {row[0]}", end=' ')
   print(f"NAME = {row[1]}", end=' ')
   print(f"AGE = {row[2]}")
   
conn.close()