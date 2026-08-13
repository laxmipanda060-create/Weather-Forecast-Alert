from app.simulator import get_simulated_weather
from app.alerts import check_alerts


print("Virtual Weather Simulation")
print("--------------------------------------")

print("Available scenarios:")
print("1. normal")
print("2. heatwave")
print("3. heavy_rain")
print("4. strong_wind")
print("5. storm")

scenario = input("\nEnter scenario: ").lower()

weather = get_simulated_weather(scenario)

if weather is not None:

    print("\nSimulated Weather")
    print("--------------------------------------")

    print("Temperature:", weather["temperature"], "°C")
    print("Humidity:", weather["humidity"], "%")
    print("Rain Probability:", weather["rain_probability"], "%")
    print("Wind Speed:", weather["wind_speed"], "km/h")

    alerts = check_alerts(
        weather["temperature"],
        weather["rain_probability"],
        weather["wind_speed"]
    )

    print("\nAlerts")
    print("--------------------------------------")

    if alerts:
        for alert in alerts:
            print(alert)
    else:
        print("✅ No weather alerts.")

else:
    print("\nInvalid scenario.")