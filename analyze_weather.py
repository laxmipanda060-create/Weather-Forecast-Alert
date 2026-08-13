import pandas as pd


file_path = "data/weather_history.csv"

try:
    df = pd.read_csv(file_path)

    print("Weather Data Analysis")
    print("--------------------------------------")

    print("\nTotal Records:", len(df))

    print("\nCollected Cities:")
    print(df["city"].unique())

    print("\nAverage Temperature:",
          round(df["temperature"].mean(), 2), "°C")

    print("Average Humidity:",
          round(df["humidity"].mean(), 2), "%")

    print("Average Wind Speed:",
          round(df["wind_speed"].mean(), 2), "km/h")

    print("\nHighest Temperature:",
          df["temperature"].max(), "°C")

    print("Lowest Temperature:",
          df["temperature"].min(), "°C")

except FileNotFoundError:
    print("Weather history file not found.")
    print("Run save_weather.py first.")