
from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("OPENWEATHER_API_KEY")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/weather")
def get_weather():
    city = request.args.get("city", "").strip()

    if not city:
        return jsonify({"error": "Please enter a city name"}), 400

    if not API_KEY:
        return jsonify({"error": "Weather API key is missing"}), 500

    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if response.status_code != 200:
            return jsonify({
                "error": data.get("message", "Unable to get weather")
            }), response.status_code

        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        description = data["weather"][0]["description"]
        wind_speed = data["wind"]["speed"]

        alerts = []

        if temperature >= 35:
            alerts.append("High temperature alert!")

        if temperature <= 5:
            alerts.append("Low temperature alert!")

        if "rain" in description.lower() or "storm" in description.lower():
            alerts.append("Rain or storm alert!")

        return jsonify({
            "city": data["name"],
            "temperature": temperature,
            "humidity": humidity,
            "description": description,
            "wind_speed": wind_speed,
            "alerts": alerts
        })

    except requests.exceptions.RequestException:
        return jsonify({
            "error": "Unable to connect to weather service"
        }), 503


if __name__ == "__main__":
    app.run(debug=True)
