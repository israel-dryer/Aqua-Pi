import psycopg2 as pg
import psutil as ps
import datetime as dt
from time import sleep
import db

def data_xfer(host, database, user, password, query):
    # loop to log temperatures, every 30 seconds for 10 minutes
    for i in range(20):

        sensors = ps.sensors_temperatures()['cpu-thermal'][0]
        time_stamp = dt.datetime.now()
        
        conn = pg.connect(host=host, database=database, user=user, password=password)

        values = [sensors.current, sensors.high, sensors.critical, time_stamp]
        c = conn.cursor()
        c.execute(query, values)
        conn.commit()
        conn.close()
        sleep(30)

def data_print():
    for i in range(20):

        sensors = ps.sensors_temperatures()['cpu-thermal'][0]
        time_stamp = dt.datetime.now()
        values = [sensors.current, sensors.high, sensors.critical, time_stamp]
        for value in values:
            print(value)
        print('-'*20,'\n')




