#!/usr/bin/python3

from datetime import datetime
import psycopg2 as psql
from config import config
import os
from model import Stuff, Job, Entity,\
    Qualification, Specialization


def init_tables():
    conn = psql.connect(**config)
    try:
        with conn.cursor() as cur:
            cur.execute(open('init_tables.sql', 'r').read())
            conn.commit()
    except Exception as ex:
        print(f'Error in init tables: {ex}')

init_tables()
    

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



