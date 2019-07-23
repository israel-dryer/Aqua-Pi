import RPi.GPIO as GPIO
from time import sleep
import Freenove_DHT as DHT
DHTPin = 11  # define the pin of DHT11

def loop():
    dht = DHT.DHT(DHTPin) # create a DHT class object
    sumCnt = 0 # number of reading times
    
    while True:
        sumCnt += 1
        chk = dht.readDHT11()
        ''' read DHT11 and get a return value. Then determine whether data read is normal
            according to read value '''
        print(f'The sumCnt is : {sumCnt}, \t chk     : {chk}')
        if chk is dht.DHTLIB_OK:
            print("DHT11, OK!")
        elif chk is dht.DHTLIB_ERROR_CHECKSUM:
            print("DHTLIB_ERROR_CHECKSUM!!")
        elif chk is dht.DHTLIB_ERROR_TIMEOUT:
            print("DHTLIB_ERROR_TIMEOUT!")
        else:
            print("Other Error!")
           
        temp = convert(dht.temperature)   
        print(f'Humidity : {dht.humidity:,.2f}, \t Temperature : {temp:,.2f}')
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
