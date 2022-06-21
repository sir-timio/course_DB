#!/usr/bin/python3

from datetime import datetime
import psycopg2 as psql
from config import config
import os
from model import Stuff, Job, Entity,\
    Qualification, Specialization


def init_tables():
    conn = psql.connect(**config)
    with conn.cursor() as cur:
        cur.execute(open('init_tables.sql', 'r').read())
        conn.commit()

init_tables()
        
    
administrators = [
    Stuff(
        id=1,
        job=Job.ADMINISTRATOR,
        name="Sasha",
        surname="Ivanova",
        salary=60_000,
        phone="89637458777"
    ),
    Stuff(
        id=2,
        job=Job.ADMINISTRATOR,
        name="Masha",
        surname="Petrova",
        salary=60_000,
        phone="89637398777"
    )
]

doctors = [
    Stuff(
        id=5,
        job=Job.DOCTOR,
        name="Ivan",
        surname="Sergev",
        license="DOC123-5123",
        salary=20_000,
        interest_rate=0.4,
        phone="89633258777"
    ),
    Stuff(
        id=6,
        job=Job.DOCTOR,
        license="DOC123-4124",
        name="Lilya",
        surname="Oslo",
        salary=20_000,
        interest_rate=0.4,
        phone="89637398777"
    )
]

nurses = [
    Stuff(
        id = 3,
        job=Job.DOCTOR,
        name="Olga",
        surname="Orlova",
        license="N412-232",
        salary=50_000,
        phone="89633268237"
    ),
    Stuff(
        id=4,
        job=Job.DOCTOR,
        license="N412-664",
        name="Ksenia",
        surname="Frolova",
        salary=50_000,
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
        stuff_id=6,
        date=datetime.now().date()
    ),
]


def insert(conn, entity: Entity):
    table_name = entity.__class__.__name__.lower()
    query = f'insert into {table_name}'
    d = entity.get_data()
    fields = d.keys()
    values = list(d.values())
    query += ' (' + ','.join(fields) + ')'
    query += ' values (' + ','.join(['%s'] * len(values)) + ')'
    print(query)
    print(values)
    try:
        with conn.cursor() as cur:
            cur.execute(query, values)
            conn.commit()
        return 1
    except Exception as ex:
        conn.rollback()
        print(f"Exeption in insert: {ex} for table {table_name} with entity {entity}")
        return 0


#add stuff
for st in stuff:
    conn = psql.connect(**config)
    insert(conn, st)        
    with psql.connect(**config).cursor() as cur:
        cur.execute('select * from stuff')
        # print(cur.fetchall())

#add qualification for doctors
for q in qualifications:
    conn = psql.connect(**config)
    insert(conn, q)
    with psql.connect(**config).cursor() as cur:
        cur.execute('select * from qualification')
        print(cur.fetchall())
        

