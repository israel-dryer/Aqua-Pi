import os
import glob
import time
import datetime as dt
import csv
import aws #aws PostgreSQL authentication

#these tow lines mount the device:
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

class DS18B20:
    def __init__(self):
        self.base_dir = r'/sys/bus/w1/devices/28*'
        self.sensor_path = []        
        self.sensor_name = []
        self.temps = []
        self.rows = []
        self.db = aws.AWS()

    def find_sensors(self):
        self.sensor_path = glob.glob(self.base_dir)
        self.sensor_name = [path.split('/')[-1] for path in self.sensor_path]

    def strip_string(self, temp_str):
        i = temp_str.index('t=')
        if i != -1:
            t = temp_str[i+2:]
            temp_c = float(t)/1000.0
            temp_f = round(temp_c * (9.0/5.0) + 32.0,3)
        return temp_c, temp_f

    def read_temp(self):
        testdate = dt.datetime.now().date()
        testtime = dt.datetime.now().time()
        for sensor, path in zip(self.sensor_name, self.sensor_path):
            # open sensor file and read data
            with open(path + '/w1_slave','r') as f:
                valid, temp = f.readlines()
            # check validity of data
            if 'YES' in valid:
                self.rows.append((testdate, testtime, sensor) + self.strip_string(temp))
                time.sleep(2)
            else:
                time.sleep(0.2)
    
    def print_temps(self):
        print('-'*90)
        for d, t, n, c, f in self.rows:
            print(f'Sensor: {n}  C={c:,.3f}  F={f:,.3f}  Date: {d}  Time: {t}')
            
    def log_csv(self):
        with open('log.csv','a+') as log:
            writer = csv.writer(log)
            writer.writerows(self.rows)
            
    def log_sql(self):
        ''' upload the data into sql db; on fail continue '''
        with open('sensor_temp_insert.sql','r') as f:
            query = f.read()
        
        with open('log.csv','r', newline='\n') as f:
            reader = csv.reader(f)
            data = [tuple(row) for row in reader]
        try:
            self.db.insert(query, data)
            return True
        except:
            return False
        
    def clear_rows(self):
        ''' clear the data from the rows list on every iteration of temp checks '''
        self.rows.clear()

def main():
    s = DS18B20()
    s.find_sensors()
    i = 1

    while True:
        s.read_temp()
        s.print_temps()
        s.log_csv()
        s.clear_rows()

        if i%10 == 0:
            upload = s.log_sql()
            if upload:
                print(f"{i} Data uploaded to SQL DB")
                f = open('log.csv','w', newline='\n')
                f.close()                
            else:
                print(f"{i} SQL upload failed. Data stored in local CSV")
        else:
                print(f"{i} Data stored in local CSV")
    
        i +=1
    
main()
