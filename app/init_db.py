#!/usr/bin/python3

import os
import sqlite3 as sql
from dataclass.model import Stuff, Specialization, Entity

DB_PATH = '../data/clinic.db'
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

class SQLite():
    def __init__(self, file='../data/clinic.db'):
        self.file=file
    def __enter__(self):
        self.conn = sql.connect(self.file)
        self.conn.row_factory = sql.Row
        return self.conn.cursor()
    def __exit__(self, type, value, traceback):
        self.conn.commit()
        self.conn.close()

with SQLite() as cur:
    cur.execute('''create table stuff
            (id            integer primary key,
            name           text    not null,
            surname        text    not null,
            specialization integer not null,
            license        integer null,
            phone          text    null,
            birth_date     text    null,
            interest_rate  real    null,
            salary         integer null
            );''')

administrators = [
    Stuff(
        specialization=Specialization.ADMINISTRATOR,
        name="Sasha",
        surname="Ivanova",
        salary=60,
        phone="89637458777"
    ),
    Stuff(
        specialization=Specialization.ADMINISTRATOR,
        name="Masha",
        surname="Petrova",
        salary=60,
        phone="89637398777"
    )
]

doctors = [
    Stuff(
        specialization=Specialization.DOCTOR,
        name="Ivan",
        surname="Sergev",
        license="DOC123-5123",
        salary=20,
        interest_rate=0.4,
        phone="89633258777"
    ),
    Stuff(
        specialization=Specialization.DOCTOR,
        license="DOC123-4124",
        name="Lilya",
        surname="Oslo",
        salary=20,
        interest_rate=0.4,
        phone="89637398777"
    )
]

nurses = [
        Stuff(
        specialization=Specialization.DOCTOR,
        name="Olga",
        surname="Orlova",
        license="N412-232",
        salary=50,
        phone="89633268237"
    ),
    Stuff(
        specialization=Specialization.DOCTOR,
        license="N412-664",
        name="Ksenia",
        surname="Frolova",
        salary=50,
        phone="89698798745"
    )
]

def get_insert_sql(entity: Entity):
    table_name = entity.__class__.__name__.lower()
    s = f'insert into {table_name}'
    d = entity.get_data()
    fields = d.keys()
    values = list(d.values())
    s += ' (' + ','.join(fields) + ')'
    s += ' values (' + ','.join(['?'] * len(values)) + ')'
    return s, values

for stuff in administrators + doctors + nurses:
    query, params = get_insert_sql(stuff)
    with SQLite() as cur:
        cur.execute(query, params)

l = ("AAA", "AAA", 3)


with SQLite() as cur:
    cur.execute('insert into stuff (name, surname, specialization) values (?, ?, ?)', l)

with SQLite() as cur:
    select = cur.execute('select id, name, surname, salary from stuff')
    for row in select:
        print(tuple(row))