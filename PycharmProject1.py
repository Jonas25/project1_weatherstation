import time,  os, Adafruit_DHT, socket, fcntl, struct
from LCDi2c import LCDi2c
from SensorReading import SensorReading
from time import gmtime, strftime

reading = SensorReading()
lcd = LCDi2c()

try:
    import ntplib
    client = ntplib.NTPClient()
    response = client.request('pool.ntp.org')
    os.system('sudo date ' + time.strftime('%m%d%H%M%Y.%S',time.localtime(response.tx_time)))
except:
    print('Could not sync with time server.')

print('Starting Up Tempature Monitor')

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('google.com', 0))
    return s.getsockname()[0]

while True:
    timest = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 6)
    hum = round(humidity, 2)
    temp = round(temperature, 2)
    lcd.lcd_string(timest, 2)
    lcd.lcd_string(get_ip_address(),1)