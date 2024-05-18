# 🌡 Termometr Raspberry Pi

![GitHub release (latest by date)](https://img.shields.io/github/v/release/bartekl1/rpi-thermometer?style=flat-square)
![GitHub Repo stars](https://img.shields.io/github/stars/bartekl1/rpi-thermometer?style=flat-square)
![GitHub watchers](https://img.shields.io/github/watchers/bartekl1/rpi-thermometer?style=flat-square)
![GitHub forks](https://img.shields.io/github/forks/bartekl1/rpi-thermometer?style=flat-square)

[🕑 Rejestr zmian](CHANGELOG_PL.md)
[🎁 Podziękowania](ACKNOWLEDGEMENTS_PL.md)

## ℹ️ O projekcie

### Dostępne czujniki

- DS18B20 (temperatura)
- DHT11 (wilgotność)

### Dostępne funkcje

- Pomiar bieżącej temperatury i wilgotności
- Zapis temperatury i wilgotności do bazy danych
- Prosta strona z bieżącymi odczytami

## 👨‍💻 Instalacja

1. Podłącz czujniki DS18B20 i DHT11 do Raspberry Pi.
2. Sklonuj repozytorium

    ```bash
    git clone https://github.com/bartekl1/rpi-thermometer
    cd rpi-thermometer
    ```

3. Utwórz bazę danych i zaimportuj jej strukturę z pliku `thermometer.sql`.

4. Utwórz plik konfiguracyjny o nazwie `configs.json` z poniższą zawartością.

    ```json
    {
        "host": "0.0.0.0",
        "mysql_user": "<mysql_user>",
        "mysql_password": "<mysql_password>",
        "mysql_database": "<mysql_database>"
    }
    ```

    Zamień `<mysql_user>`, `<mysql_password>` i `<mysql_database>` na prawidłowe dane logowania.

5. Zainstaluj zależności PIP.

    ```bash
    pip install -r requirements.txt
    ```

6. Utwórz plik `/etc/systemd/system/thermometer.service` z poniższą zawartością.

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

    Zamień `<PATH>` na ścieżkę do sklonowanego repozytorium i `<USERNAME>` na systemową nazwę użytkownika.

7. Uruchom i włącz automatyczne uruchamianie utworzonej usługi.

    ```bash
    sudo systemctl start thermometer
    sudo systemctl enable thermometer
    ```

8. Dodaj poniższą linię do crontab (edytuj za pomocą polecenia `crontab -e`).

    ```text
    */10 * * * * cd "<PATH>" && python3 save_to_database.py
    ```

    Zamień `<PATH>` na ścieżkę do sklonowanego repozytorium. Możesz zmienić wyrażenie cron, aby zmienić częstotliwość.
