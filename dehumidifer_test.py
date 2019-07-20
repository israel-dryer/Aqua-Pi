import RPi.GPIO as GPIO
from time import sleep
import Freenove_DHT as DHT
import dehumidifier as dm
DHTPin = 11  # define the pin of DHT11

def loop():
    dht = DHT.DHT(DHTPin) # create a DHT class object
    dhm = dm.DeHumidifier()
    
    while True:
        chk = dht.readDHT11()
        if chk is dht.DHTLIB_OK:
            temp = convert(dht.temperature)
            dhm.check_status(dht)
            print(f'Humidity : {dht.humidity:,.2f}, \t Temperature : {temp:,.2f}')
        else:
            pass
               
        sleep(2)
        
def convert(temp):
    ''' Convert a celcius temperature reading to fahrenheit '''
    try:
        fh = (temp * 9/5) + 32
        return fh
    except ValueError:
        return 0
    
if __name__ == '__main__':
    print('Program is starting...')
    try:
        loop()
    except KeyboardInterrupt:
        GPIO.cleanup()
        exit()
