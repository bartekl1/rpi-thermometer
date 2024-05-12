function setTemperature() {
    fetch("/api/temperature").then((response) => { return response.json() }).then((json) => {
        if (json.status === "ok" && json.temperature !== null) {
            document.querySelector("#temperature").innerHTML = `${json.temperature.toFixed(1)}°C`;
        } else {
            document.querySelector("#temperature").innerHTML = "--";
        }
    }).catch(() => {
        document.querySelector("#temperature").innerHTML = "--";
    })
}

function setHumidity() {
    fetch("/api/humidity").then((response) => { return response.json() }).then((json) => {
        if (json.status === "ok" && json.humidity !== null) {
            document.querySelector("#humidity").innerHTML = `${json.humidity.toFixed(0)}%`;
        } else {
            document.querySelector("#humidity").innerHTML = "--";
        }
    }).catch(() => {
        document.querySelector("#humidity").innerHTML = "--";
    })
}

setInterval(setTemperature, 30_000);
setInterval(setHumidity, 30_000);

setTemperature();
setHumidity();

console.log(
    "%cRaspberry Pi Thermometer\n\n%cby @bartekl1\nv. 1.0\n\n%chttps://github.com/bartekl1/rpi-thermometer",
    "font-size: 36px; font-weight: 600;",
    "font-size: 16px;",
    "font-size: 14px;"
);
