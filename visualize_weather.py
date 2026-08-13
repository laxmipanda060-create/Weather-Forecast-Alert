import pandas as pd
import matplotlib.pyplot as plt


file_path = "data/weather_history.csv"

df = pd.read_csv(file_path)

df["timestamp"] = pd.to_datetime(df["timestamp"])


# --------------------------------------
# Temperature Chart
# --------------------------------------

plt.figure(figsize=(10, 5))

plt.plot(
    df["timestamp"],
    df["temperature"],
    marker="o"
)

plt.title("Temperature History")
plt.xlabel("Date and Time")
plt.ylabel("Temperature (°C)")

plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig("charts/temperature_history.png")

plt.close()

print("Temperature chart saved.")


# --------------------------------------
# Humidity Chart
# --------------------------------------

plt.figure(figsize=(10, 5))

plt.plot(
    df["timestamp"],
    df["humidity"],
    marker="o"
)

plt.title("Humidity History")
plt.xlabel("Date and Time")
plt.ylabel("Humidity (%)")

plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig("charts/humidity_history.png")

plt.close()

print("Humidity chart saved.")


# --------------------------------------
# Wind Speed Chart
# --------------------------------------

plt.figure(figsize=(10, 5))

plt.plot(
    df["timestamp"],
    df["wind_speed"],
    marker="o"
)

plt.title("Wind Speed History")
plt.xlabel("Date and Time")
plt.ylabel("Wind Speed (km/h)")

plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig("charts/wind_speed_history.png")

plt.close()

print("Wind speed chart saved.")


print("\nAll charts generated successfully!")
# --------------------------------------
# City Temperature Comparison
# --------------------------------------

city_temperature = df.groupby("city")["temperature"].mean()

plt.figure(figsize=(10, 5))

city_temperature.plot(
    kind="bar"
)

plt.title("Average Temperature by City")
plt.xlabel("City")
plt.ylabel("Average Temperature (°C)")

plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig("charts/city_temperature_comparison.png")

plt.close()

print("City comparison chart saved.")