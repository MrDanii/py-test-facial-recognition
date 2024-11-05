import sys
import psycopg2
from databaseconf.config_db import load_config


def insertEmbedding(embeddings=[]):
    sql = """INSERT INTO "AddressPersonImage"(embeddings)
             VALUES(%s) RETURNING "idAddressPersonImage";"""
    
    idAddressPersonImage = None
    config = load_config()

    try:
        print('algo')
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                #* Execute Insert
                #* Note: putting a "," it's important, this is how python interpret this is a tuple
                cur.execute(sql, (embeddings,))

                #* Get last ID
                firstRow = cur.fetchone()
                if firstRow:
                    idAddressPersonImage = firstRow[0]
                
                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error, file=sys.stderr)
    finally:
        return idAddressPersonImage

