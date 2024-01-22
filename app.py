from flask import Flask, redirect, url_for
import pytz
import tzlocal

from w1thermsensor import W1ThermSensor

import json
import datetime

with open('configs.json') as file:
    configs = json.load(file)

app = Flask(__name__)

w1_sensor = None


def load_sensors():
    global w1_sensor

    try:
        w1_sensor.get_temperature()
    except Exception:
        try:
            w1_sensor = W1ThermSensor()
        except Exception:
            pass


try:
    load_sensors()
except Exception:
    pass


@app.route('/')
def index():
    return redirect(url_for('get_temperature'))


@app.route('/api/temperature')
def get_temperature():
    try:
        load_sensors()
    except Exception:
        pass

    try:
        w1_temperature = w1_sensor.get_temperature()
    except Exception:
        temperature = None
    else:
        temperature = w1_temperature

    tz_name = str(tzlocal.get_localzone())
    tz = pytz.timezone(tz_name)
    dt = tz.localize(datetime.datetime.now())
    iso = dt.isoformat()

    return {
        "status": "ok",
        "date": iso,
        "temperature": temperature
    }


if __name__ == '__main__':
    debug = configs['debug'] if 'debug' in configs.keys() else None
    host = configs['host'] if 'host' in configs.keys() else None
    port = configs['port'] if 'port' in configs.keys() else None

    app.run(debug=debug, host=host, port=port)
