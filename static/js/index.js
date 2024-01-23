function setTemperature() {
    fetch("/api/temperature").then((response) => { return response.json() }).then((json) => {
        if (json.status === "ok" && json.temperature !== null) {
            document.querySelector("#temperature").innerHTML = `${json.temperature.toFixed(1)}℃`;
        } else {
            document.querySelector("#temperature").innerHTML = "--";
        }
    }).catch(() => {
        document.querySelector("#temperature").innerHTML = "--";
    })
}

setInterval(setTemperature, 30_000);

setTemperature();
