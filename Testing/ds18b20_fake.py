import os
import glob
import time
import csv
import datetime as dt

#these tow lines mount the device:
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

class Sensor:
    def __init__(self):
        '''
        A class to retrieve and process the DS18B20 sensor with a Raspberry Pi. The only methods that you really need to
        work with are listed below. All of the others are helper functions:
        
        - collect_data()
        - load_data()
        
        The load data method assumes that you want to upload the data into a database, so the data is return as a `dict`.
        '''
        self.base_dir = r'/home/pi/Documents/Aqua-Pi/Testing/28*'
        self.sensor_path = []        
        self.sensor_name = []
        self.temps = []
        self.rows = []
        
    def strip_string(self, temp_str):
        '''
        Strips the temperature data from the string returns by the temperature reading
        
        Parameters
        ----------
        temp_str : `string`
            The temperature string returns by the sensor
            
        Returns
        -------
        temp_c : `float`
            temperature in degrees celsius
        temp_f : `float`
            temperate in degree fahrenheit
            
        '''
        i = temp_str.index('t=')
        if i != -1:
            t = temp_str[i+2:]
            temp_c = float(t)/1000.0
            temp_f = round(temp_c * (9.0/5.0) + 32.0,3)
        return temp_c, temp_f        

    def find_sensors(self):
        ''' Locate each sensor instance and store the name and path '''
        self.sensor_path = glob.glob(self.base_dir)
        self.sensor_name = [path.split('/')[-1] for path in self.sensor_path]

    def read_data(self):
        ''' Open the sensor file located from the `find_sensors()` method and pull the data '''
        testdate = dt.datetime.now().date()
        testtime = dt.datetime.now().time()
        
        for sensor, path in zip(self.sensor_name, self.sensor_path):
            # open sensor file and read data
            with open(path + '/w1_slave','r') as f:
                valid, temp = f.readlines()
            # check validity of data
            if 'YES' in valid:
                self.rows.append((testdate, testtime, sensor) + self.strip_string(temp))
            else:
                time.sleep(0.2)
                
    def log_csv(self, name='log.csv'):
        '''
        Create a temporary log that stores the sensor data in a csv file until uploaded to
        a more permanent source.
        
        Parameters
        ----------
        name : `string`
            The name of the csv file that you want to log
        '''
        with open(name,'a+') as log:
            writer = csv.writer(log)
            writer.writerows(self.rows)
            
    def clear_rows(self):
        ''' clear the data from the rows list on every iteration of temp checks '''
        self.rows.clear()            
                
    def collect_data(self):
        '''A wrapper around the data collection methods'''
        self.find_sensors()
        self.read_data()
        self.log_csv()
        self.print_data()
        self.clear_rows()
    
    def print_data(self):
        ''' Nicely formatted data string '''
        print('-'*90)
        for d, t, n, c, f in self.rows:
            print(f'Sensor: {n}  C={c:,.3f}  F={f:,.3f}  Date: {d}  Time: {t}')
            
    def load_data(self, file='log.csv', name='SensorTemps'):
        '''
        Load the data into csv and return dict. For uploading into another source, such as
        a database. The default import file is 'log.csv', and the default name is 'SensorTemps'
        
        Parameters
        -----------
        file : `string` (optional)
            The name of the sensor data file you want to upload
        name : `string` (optional)
            The name of the data. This will correspond to a table name if uploading to database
        
        Returns
        --------
        data : `dict`
            Sensor data in the pattern of {name : data}
        
        '''
        with open('log.csv','r', newline='\n') as f:
            reader = csv.reader(f)
            data = {name:[tuple(row) for row in reader]}
            return data
        
    def purge_csv(self, name='log.csv'):
        '''
        Purge the data from the staging csv file
        
        Parameters
        ----------
        name : `string`
            The name of the csv file that you want to log
        '''
        f = open(name,'w')
        f.close()