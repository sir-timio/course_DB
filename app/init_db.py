#!/usr/bin/python3

from datetime import datetime
import os
import sqlite3 as sql
from dataclass.model import Stuff, Job, Entity,\
    Qualification, Specialization

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
    cur.execute(
        '''
        create table qualification(
        id              integer primary key,
        organization    text    not null,
        specialization  integer not null,
        date            text    null,
        description     text    null,
        stuff_id        integer not null,
        foreign key (stuff_id) references stuff(id)
        );
        ''')

        
    
administrators = [
    Stuff(
        job=Job.ADMINISTRATOR,
        name="Sasha",
        surname="Ivanova",
        salary=60,
        phone="89637458777"
    ),
    Stuff(
        job=Job.ADMINISTRATOR,
        name="Masha",
        surname="Petrova",
        salary=60,
        phone="89637398777"
    )
]

doctors = [
    Stuff(
        job=Job.DOCTOR,
        name="Ivan",
        surname="Sergev",
        license="DOC123-5123",
        salary=20,
        interest_rate=0.4,
        phone="89633258777"
    ),
    Stuff(
        job=Job.DOCTOR,
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
        job=Job.DOCTOR,
        name="Olga",
        surname="Orlova",
        license="N412-232",
        salary=50,
        phone="89633268237"
    ),
    Stuff(
        job=Job.DOCTOR,
        license="N412-664",
        name="Ksenia",
        surname="Frolova",
        salary=50,
        phone="89698798745"
    )
]

stuff = administrators + doctors + nurses

qualifications = [
    Qualification(
        specialization=Specialization.ORTHODONTIST, 
        organization='Ural med', 
        stuff_id=5,
        date=datetime.now().date()
    ),
    Qualification(
        specialization=Specialization.SURGEON, 
        organization='Moscow med', 
        stuff_id=10,
        date=datetime.now().date()
    ),
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

for st in stuff:
    query, params = get_insert_sql(st)
    with SQLite() as cur:
        cur.execute(query, params)

for qual in qualifications:
    
    query, params = get_insert_sql(qual)
    print(params)
    with SQLite() as cur:
        cur.execute(query, params)


with SQLite() as cur:
    select = cur.execute('select * from stuff')
    for row in select:
        print(tuple(row))

with SQLite() as cur:
    select = cur.execute('select * from qualification')
    for row in select:
        print(tuple(row))
with SQLite() as cur:
    s = cur.execute('PRAGMA foreign_keys;')
    for r in s:
        print(tuple(r))