import Adafruit_DHT, helper
from LCDi2c import LCDi2c
from SensorReading import SensorReading
from time import gmtime, strftime

reading = SensorReading()
lcd = LCDi2c()

helper.sync_time()

print('Starting Up Tempature Monitor')

while True:
    timest = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 6)
    hum = round(humidity, 2)
    temp = round(temperature, 2)
    lcd.lcd_string(timest, 2)
    lcd.lcd_string(helper.get_ip_address(), 1)
