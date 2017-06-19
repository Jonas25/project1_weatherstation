import threading, serial, time, Adafruit_DHT
from dbconn import DbConnection
from time import gmtime, strftime
from serial import SerialException

class SensorReading(threading.Thread):
    def __init__(self, interval=1):
        super(SensorReading, self).__init__()
        self.interval = interval

        self.db = DbConnection(database="weatherstation")
        #self.humidity_in, self.temperature_in = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 24)

        try:
            self.ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=.5)
            thread = threading.Thread(target=self.run, args=())
            thread.daemon = True
            thread.start()
        except SerialException:
            print("Could not open port /dev/ttyUSB0")
            self._stop()

    def _stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        while True:
            try:
                while self.ser.inWaiting():
                    incoming = self.ser.readline().strip().decode("ascii")
                    print('Received data: ' + incoming)
                    array = incoming.split(",")
                    if len(array) == 6:
                        timest = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                        for x in range(0,10,2):
                            sql = (
                                'INSERT INTO weatherstation.measurement (SensorID, Value, TimeStamp)'
                                'VALUES ( %(sensorid)s, %(value)s, %(timestamp)s );'
                            )
                            params = {
                                'sensorid': array[x],
                                'value': array[x+1],
                                'timestamp': timest,
                            }
                            self.db.execute(sql, params)
                    time.sleep(1)
                    self.ser.write(bytearray("1","ascii"))
                    # self.humidity_in = round(self.humidity_in, 2)
                    # self.temperature_in = round(self.temperature_in, 2)
                    # timest = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                    # sql1 = (
                    #     'INSERT INTO weatherstation.measurement (SensorID, Value, TimeStamp)'
                    #     'VALUES ( %(sensorid)s, %(value)s, %(timestamp)s );'
                    # )
                    # params1 = {
                    #     'sensorid': '1',
                    #     'value': self.temperature_in,
                    #     'timestamp': timest,
                    # }
                    # sql2 = (
                    #     'INSERT INTO weatherstation.measurement (SensorID, Value, TimeStamp)'
                    #     'VALUES ( %(sensorid)s, %(value)s, %(timestamp)s );'
                    # )
                    # params2 = {
                    #     'sensorid': '2',
                    #     'value': self.humidity_in,
                    #     'timestamp': timest,
                    # }
                    # self.db.execute(sql1, params1)
                    # self.db.execute(sql2, params2)
            except KeyboardInterrupt:
                self.ser.close()
                break
            except IOError:
                self.ser.close()
                print("USB antenna disconnected, connect USB antenna and restart system")
                break
            time.sleep(self.interval)