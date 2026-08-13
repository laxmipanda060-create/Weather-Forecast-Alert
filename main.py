from app.api import get_coordinates, get_weather
from app.alerts import check_alerts


print("Weather Forecast & Alert Application")
print("--------------------------------------")

city = input("Enter city name: ")

location = get_coordinates(city)

if location is not None:

    print("\nLocation found:")
    print("City:", location["name"])

    weather = get_weather(
        location["latitude"],
        location["longitude"]
    )

    if weather is not None:

        current = weather["current"]
        daily = weather["daily"]

        print("\nCurrent Weather")
        print("--------------------------------------")
        print("Temperature:", current["temperature_2m"], "°C")
        print("Humidity:", current["relative_humidity_2m"], "%")
        print("Wind Speed:", current["wind_speed_10m"], "km/h")

        print("\nWeather Alerts")
        print("--------------------------------------")

        alerts = check_alerts(
            current["temperature_2m"],
            daily["precipitation_probability_max"][0],
            current["wind_speed_10m"]
        )

        if alerts:
            for alert in alerts:
                print(alert)
        else:
            print("✅ No weather alerts.")

        print("\n7-Day Forecast")
        print("--------------------------------------")

        for i in range(7):
            print(
                daily["time"][i],
                "| Max:",
                daily["temperature_2m_max"][i],
                "°C",
                "| Min:",
                daily["temperature_2m_min"][i],
                "°C",
                "| Rain:",
                daily["precipitation_probability_max"][i],
                "%"
            )

    else:
        print("\nUnable to get weather data.")

else:
    print("\nCity not found.")