import sys
import psycopg2
from databaseconf.config_db import load_config


def connect(config):
    """ Connect to the PostgreSQL database server """
    try:
        # connecting to the PostgreSQL server
        with psycopg2.connect(**config) as conn:
            print(
                'Connected to the PostgreSQL server - Facial Recognition Database Working.', file=sys.stderr)
            return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(error, file=sys.stderr)


if __name__ == '__main__':
    config = load_config()
    connect(config)
