class DeHumidifier:
    ''' Represents an air conditioner unit '''
    
    def __init__(self):
        self.power = False
        self.target = 75.00
    
    def power_on(self):
        self.power = True
        
    def power_off(self):
        self.power = False
        
    def set_target(self, target):
        try:
            self.target = float(target)
        except ValueError:
            print('Enter number values only!')
            pass
        
    def check_status(self, sensor):
        ''' check humidity vs target and adjust power settings if different than expected '''
        if sensor.humidity > self.target:
            if not self.power:
                self.power_on()
                print(f'ALERT!!  Humidity {sensor.humidity:,.2f} exceeds target {self.target:,.2f}; Humidifier has been powered ON.')
            else:
                pass
        else:
            if self.power:
                self.power_off()
                print(f'ALERT!!  Humidity {sensor.humidity:,.2f} is below target {self.target:,.2f}; Humidifier has been powered OFF.')
            else:
                pass
            
