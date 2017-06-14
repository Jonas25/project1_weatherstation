import threading
import serial, time
from dbconn import DbConnection
from time import gmtime, strftime

db = DbConnection(database="weatherstation")
ser = serial.Serial('/dev/ttyUSB0',9600,timeout=.5)

class SensorReading(object):
    def __init__(self, interval=1):
        self.interval = interval

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        while True:
            try:
                while ser.inWaiting():
                    incoming = ser.readline().strip().decode("ascii")
                    print('Received data: ' + incoming)
                    array = incoming.split(",")
                    #print(len(array))
                    #print(array)
                    if len(array) == 6:
                        timest = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                        for x in range(0,6,2):
                            sql = (
                                'INSERT INTO weatherstation.measurement (SensorID, Value, TimeStamp)'
                                'VALUES ( %(sensorid)s, %(value)s, %(timestamp)s );'
                            )
                            params = {
                                'sensorid': array[x],
                                'value': array[x+1],
                                'timestamp': timest,
                            }
                            result = db.execute(sql, params)
                            print(result)
                    time.sleep(1)
                    ser.write(bytearray("1","ascii"))
            except KeyboardInterrupt:
                ser.close()
                break
            time.sleep(self.interval)