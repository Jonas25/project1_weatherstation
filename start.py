import helper, os
from flask import Flask
from flask import render_template
from SensorReading import SensorReading
from LCDi2c import LCDi2c
from datetime import datetime
from dbconn import DbConnection

try:
    reading = SensorReading()
except Exception:
    print("An error occurred while starting the sensors")

app = Flask(__name__)
lcd = LCDi2c()
db = DbConnection(database="weatherstation")

helper.sync_time()

print('Starting Up Weather Station')
i = datetime.now()
lcd.lcd_string(helper.get_ip_address(), 1)
lcd.lcd_string(str(i.day)+"-"+str(i.month)+"-"+str(i.year), 2)

@app.route('/')
def dashboard():
    sql = (
        'SELECT * FROM weatherstation.measurement WHERE SensorID=%(sensorid)s;'
    )
    params = {
        'sensorid': '3',
    }
    data_temp = db.query(sql, params)
    sql = (
        'SELECT * FROM weatherstation.measurement WHERE SensorID=%(sensorid)s;'
    )
    params = {
        'sensorid': '4',
    }
    data_hum = db.query(sql, params)
    sql = (
        'SELECT * FROM weatherstation.measurement WHERE SensorID=%(sensorid)s ORDER BY ID DESC LIMIT 1;'
    )
    params = {
        'sensorid': '3',
    }
    last_temp_out = db.query(sql, params)
    sql = (
        'SELECT * FROM weatherstation.measurement WHERE SensorID=%(sensorid)s ORDER BY ID DESC LIMIT 1;'
    )
    params = {
        'sensorid': '4',
    }
    last_hum_out = db.query(sql, params)
    return render_template('index.html',data_temp=data_temp, data_hum=data_hum, last_temp_out=last_temp_out, last_hum_out=last_hum_out)


@app.route('/contact')
def contact():
    return "Contact pagina"


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5050))
    host = "0.0.0.0"
    app.run(host=host, port=port, debug=True)