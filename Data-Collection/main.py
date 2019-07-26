from logger_aws import *
from ds18b20 import *
from time import sleep


sensor = Sensor()
logger = Logger(user='USERNAME', password='PASSWORD') # <--- ENTER YOUR USER NAME AND PASSWORD HERE
i = 1

while True:
    # load the data into the database after 10 iterations
    if i%10 != 0: 
        sensor.collect_data()
        sensor.log_csv()
        sleep(1) # 30 second delay between measurements
        i+=1
    else:
        data = sensor.load_data()
        status = logger.log_data(data)
        if status:
            sensor.purge_csv()
        else:
            pass
        i+=1