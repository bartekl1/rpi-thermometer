# 🌡 Raspberry Pi Thermometer

![GitHub release (latest by date)](https://img.shields.io/github/v/release/bartekl1/rpi-thermometer?style=flat-square)
![GitHub Repo stars](https://img.shields.io/github/stars/bartekl1/rpi-thermometer?style=flat-square)
![GitHub watchers](https://img.shields.io/github/watchers/bartekl1/rpi-thermometer?style=flat-square)
![GitHub forks](https://img.shields.io/github/forks/bartekl1/rpi-thermometer?style=flat-square)

[🕑 Changelog](CHANGELOG.md)
[🎁 Acknowledgements](ACKNOWLEDGEMENTS.md)
[🇵🇱 Polish version of README](README_PL.md)

## ℹ️ About

### Available sensors

- DS18B20 (temperature)
- DHT11 (humidity)

### Available functions

- Measure current temperature and humidity
- Save temperature and humidity to database
- Simple website with current readings

## 👨‍💻 Installation

1. Connect the DS18B20 and DHT11 sensors to the Raspberry Pi.
2. Clone repository

    ```bash
    git clone https://github.com/bartekl1/rpi-thermometer
    cd rpi-thermometer
    ```

3. Create database and import structure from `thermometer.sql` file.

4. Create configuration file named `configs.json` with the following content.

    ```json
    {
        "host": "0.0.0.0",
        "mysql_user": "<mysql_user>",
        "mysql_password": "<mysql_password>",
        "mysql_database": "<mysql_database>"
    }
    ```

    Replace `<mysql_user>`, `<mysql_password>` and `<mysql_database>` with correct credentials.

5. Install PIP dependencies.

    ```bash
    pip install -r requirements.txt
    ```

6. Create `/etc/systemd/system/thermometer.service` file with the following content.

    ```ini
    [Unit]
    Description=Thermometer
    After=network.target

    [Service]
    WorkingDirectory=<PATH>
    ExecStart=/usr/bin/python3 <PATH>/app.py
    Restart=always
    User=<USERNAME>

    [Install]
    WantedBy=multi-user.target
    ```

    Replace `<PATH>` with path to the cloned repository and `<USERNAME>` with your system username.

7. Start and enable created service.

    ```bash
    sudo systemctl start thermometer
    sudo systemctl enable thermometer
    ```

8. Add following line to crontab (edit using `crontab -e`).

    ```text
    */10 * * * * cd "<PATH>" && python3 save_to_database.py
    ```

    Replace `<PATH>` with path to the cloned repository. You can edit cron expression to change frequency.
