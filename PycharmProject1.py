import serial, time, datetime, sys, Adafruit_DHT
from LCDi2c import LCDi2c
#from xbee import XBee

ser = serial.Serial('/dev/ttyUSB0',9600,timeout=.5)
lcd = LCDi2c()
#xbee = XBee(ser)

print('Starting Up Tempature Monitor')
# Continuously read and print packets
while True:
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 6)
    hum = round(humidity, 2)
    temp = round(temperature, 2)
    lcd.lcd_string(str(hum), 2)
    try:
        while ser.inWaiting():
            #ser.write('Hello from Raspberry\r\n')
            incoming = ser.readline().strip()
            print('Received data: ' + incoming)
            lcd.lcd_string(incoming,1)
    except KeyboardInterrupt:
        ser.close()
        break

ser.close()