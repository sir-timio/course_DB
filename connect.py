#!/usr/bin/python

import psycopg2
from app.config import config

print(config)

try:
    conn = psycopg2.connect(**config)

    with conn.cursor() as cur:
        cur.execute('select version();')
        print(cur.fetchone())
except Exception as e:
    print(e)
    print("Error")
