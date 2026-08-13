def get_simulated_weather(scenario):
    scenarios = {
        "normal": {
            "temperature": 30,
            "humidity": 65,
            "rain_probability": 20,
            "wind_speed": 15
        },

        "heatwave": {
            "temperature": 43,
            "humidity": 35,
            "rain_probability": 10,
            "wind_speed": 12
        },

        "heavy_rain": {
            "temperature": 28,
            "humidity": 90,
            "rain_probability": 90,
            "wind_speed": 20
        },

        "strong_wind": {
            "temperature": 29,
            "humidity": 60,
            "rain_probability": 30,
            "wind_speed": 50
        },

        "storm": {
            "temperature": 35,
            "humidity": 85,
            "rain_probability": 95,
            "wind_speed": 60
        }
    }

    return scenarios.get(scenario)