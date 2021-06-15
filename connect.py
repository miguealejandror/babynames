import psycopg2
from config import config
def connect():
    """ Conexion a PostgreSQL database server """
    try:
        params = config()
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        
	    #Prueba
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        #Mostrando Prueba
        db_version = cur.fetchone()
        print(db_version)

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return conn