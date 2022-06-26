#!/usr/bin/python3

import psycopg2 as psql
from config import config


def init_tables():
    conn = psql.connect(**config)
    try:
        with conn.cursor() as cur:
            cur.execute(open('init_tables.sql', 'r').read())
            conn.commit()
    except Exception as ex:
        print(f'Error in init tables: {ex}')

init_tables()
    
