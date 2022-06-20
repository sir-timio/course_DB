#!/usr/bin/python

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
        job=Job.ADMINISTRATOR,
        name="Sasha",
        surname="Ivanova",
        salary=60_000,
        phone="89637458777"
    ),
    Stuff(
        job=Job.ADMINISTRATOR,
        name="Masha",
        surname="Petrova",
        salary=60_000,
        phone="89637398777"
    )
]

doctors = [
    Stuff(
        job=Job.DOCTOR,
        name="Ivan",
        surname="Sergev",
        license="DOC123-5123",
        salary=20_000,
        interest_rate=0.4,
        phone="89633258777"
    ),
    Stuff(
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
        job=Job.DOCTOR,
        name="Olga",
        surname="Orlova",
        license="N412-232",
        salary=50_000,
        phone="89633268237"
    ),
    Stuff(
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
        stuff_id=3,
        date=datetime.now().date()
    ),
    Qualification(
        specialization=Specialization.SURGEON, 
        organization='Moscow med', 
        stuff_id=4,
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
        print(f"Exeption in insert func: {ex} for table {table_name}")
        return 0

for st in stuff:
    conn = psql.connect(**config)
    insert(conn, st)        
    with psql.connect(**config).cursor() as cur:
        cur.execute('select * from stuff')
        # print(cur.fetchall())

for q in qualifications:
    conn = psql.connect(**config)
    insert(conn, q)
    with psql.connect(**config).cursor() as cur:
        cur.execute('select * from qualification')
        print(cur.fetchall())
        
