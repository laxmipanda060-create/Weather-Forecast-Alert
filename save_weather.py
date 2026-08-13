import os
import pandas as pd
from datetime import datetime

from app.api import get_coordinates, get_weather


print("Weather Data Collection")
print("--------------------------------------")

city = input("Enter city name: ")

location = get_coordinates(city)

if location is not None:

    weather = get_weather(
        location["latitude"],
        location["longitude"]
    )

    if weather is not None:

        current = weather["current"]

        data = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "city": location["name"],
            "latitude": location["latitude"],
            "longitude": location["longitude"],
            "temperature": current["temperature_2m"],
            "humidity": current["relative_humidity_2m"],
            "wind_speed": current["wind_speed_10m"]
        }

        df = pd.DataFrame([data])

        file_path = "data/weather_history.csv"

        file_exists = os.path.exists(file_path)

        df.to_csv(
            file_path,
            mode="a",
            header=not file_exists,
            index=False
        )

        print("\nWeather data saved successfully!")
        print("File:", file_path)

    else:
        print("\nUnable to get weather data.")

else:
    print("\nCity not found.")