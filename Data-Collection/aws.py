import psycopg2 as pg

class AWS:
    def __init__(self):
       pass
       
    def insert(self, query, params):
        conn = pg.connect(host='aquapi.c5uh7gzya75b.us-east-2.rds.amazonaws.com',
                          user='pyadmin',
                          password='rewuio&7')
        cursor = conn.cursor()
        cursor.executemany(query, params)
        conn.commit()
        conn.close()
    
    def execute(self, query):
        conn = pg.connect(host='aquapi.c5uh7gzya75b.us-east-2.rds.amazonaws.com',
                          user='pyadmin',
                          password='rewuio&7')
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        conn.close()

    # use the following format to write a query with multiple paramters in PostGreSQL
    # INSERT INTO temperatures(current, high, critical, timestamp) VALUES(%s, %s, %s, %s)

    