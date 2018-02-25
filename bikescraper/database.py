import json

import psycopg2


TABLE_NAME = 'bike_positions'


def get_connection(config):
  return psycopg2.connect(**config)


def create_table(curs):
  curs.execute(f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
      id BIGSERIAL PRIMARY KEY,
      provider VARCHAR(10),
      positions JSON,
      created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT (NOW() AT TIME ZONE 'utc')
    );""")


def insert_positions(curs, provider, positions):
  curs.execute(f"""
    INSERT INTO {TABLE_NAME} (provider, positions)
    VALUES (%s, %s)""", (provider, json.dumps(positions)))
