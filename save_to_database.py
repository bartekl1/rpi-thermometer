import mysql.connector
import requests

import json

with open("configs.json") as file:
    configs = json.load(file)

    mysql_configs = {}
    if "mysql_host" in configs.keys():
        mysql_configs["host"] = configs["mysql_host"]
    if "mysql_port" in configs.keys():
        mysql_configs["port"] = configs["mysql_port"]
    if "mysql_user" in configs.keys():
        mysql_configs["user"] = configs["mysql_user"]
    if "mysql_password" in configs.keys():
        mysql_configs["password"] = configs["mysql_password"]
    if "mysql_database" in configs.keys():
        mysql_configs["database"] = configs["mysql_database"]

    port = configs["port"] if "port" in configs.keys() else 5000


def main():
    try:
        r1 = requests.get(f"http://localhost:{port}/api/temperature")
        r1j = r1.json()
        temperature = r1j["temperature"]
    except Exception:
        temperature = None

    try:
        r2 = requests.get(f"http://localhost:{port}/api/humidity")
        r2j = r2.json()
        humidity = r2j["humidity"]
    except Exception:
        humidity = None

    if temperature is not None or humidity is not None:
        db = mysql.connector.connect(**mysql_configs)
        cursor = db.cursor(dictionary=True)
        cursor.execute("INSERT INTO readings (temperature, humidity) VALUES (%s, %s)", (temperature, humidity))
        db.commit()
        cursor.close()
        db.close()


if __name__ == "__main__":
    main()
