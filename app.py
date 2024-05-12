from flask import Flask, render_template, send_file
import pytz
import tzlocal

from w1thermsensor import W1ThermSensor
import adafruit_dht
import board

import json
import datetime
import time
import threading

with open('configs.json') as file:
    configs = json.load(file)

app = Flask(__name__)

temperature = None
temperature_loaded = None
humidity = None
humidity_loaded = None


def measure_temperature():
    global temperature, temperature_loaded
    sensor_loaded = False
    sensor = None
    while not sensor_loaded:
        try:
            sensor = W1ThermSensor()
        except Exception:
            time.sleep(1)
        else:
            sensor_loaded = True
    while True:
        try:
            temperature = sensor.get_temperature()
            temperature_loaded = datetime.datetime.now()
        except Exception:
            if temperature_loaded is not None and \
               (datetime.datetime.now() - temperature_loaded).seconds > 60:
                temperature = None
                temperature_loaded = None
        time.sleep(1)


def measure_humidity():
    global humidity, humidity_loaded
    sensor_loaded = False
    sensor = None
    while not sensor_loaded:
        try:
            sensor = adafruit_dht.DHT11(board.D17)
        except Exception:
            time.sleep(1)
        else:
            sensor_loaded = True
    while True:
        try:
            humidity = sensor.humidity
            humidity_loaded = datetime.datetime.now()
        except Exception:
            if humidity_loaded is not None and \
               (datetime.datetime.now() - humidity_loaded).seconds > 60:
                humidity = None
                humidity_loaded = None
        time.sleep(1)


@app.before_first_request
def start_thread():
    temperature_measure_thread = threading.Thread(target=measure_temperature)
    humidity_measure_thread = threading.Thread(target=measure_humidity)
    temperature_measure_thread.start()
    humidity_measure_thread.start()


@app.route('/favicon.ico')
def favicon():
    return send_file('static/img/icon_x128.ico')


@app.route('/manifest.json')
def manifest():
    return send_file('static/manifest.json')


@app.route('/manifest_pl.json')
def manifest_pl():
    return send_file('static/manifest_pl.json')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/temperature')
def get_temperature():
    global temperature, temperature_loaded

    if temperature is not None:
        tz_name = str(tzlocal.get_localzone())
        tz = pytz.timezone(tz_name)
        dt = tz.localize(temperature_loaded)
        iso = dt.isoformat()

        return {
            "status": "ok",
            "date": iso,
            "temperature": temperature
        }
    else:
        return {
            "status": "error",
            "date": None,
            "temperature": None
        }


@app.route('/api/humidity')
def get_humidity():
    global humidity, humidity_loaded

    if humidity is not None:
        tz_name = str(tzlocal.get_localzone())
        tz = pytz.timezone(tz_name)
        dt = tz.localize(humidity_loaded)
        iso = dt.isoformat()

        return {
            "status": "ok",
            "date": iso,
            "humidity": humidity
        }
    else:
        return {
            "status": "error",
            "date": None,
            "humidity": None
        }


if __name__ == '__main__':
    debug = configs['debug'] if 'debug' in configs.keys() else None
    host = configs['host'] if 'host' in configs.keys() else None
    port = configs['port'] if 'port' in configs.keys() else None

    app.run(debug=debug, host=host, port=port)
