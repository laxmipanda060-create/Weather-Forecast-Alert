import csv
import os
from datetime import datetime

from app.logger import logger


# ============================================================
# DATA DIRECTORY
# ============================================================

DATA_DIRECTORY = "data"

os.makedirs(
    DATA_DIRECTORY,
    exist_ok=True
)


# ============================================================
# WEATHER HISTORY FILE
# ============================================================

WEATHER_HISTORY_FILE = os.path.join(
    DATA_DIRECTORY,
    "weather_history.csv"
)


# ============================================================
# CSV HEADERS
# ============================================================

CSV_HEADERS = [
    "timestamp",
    "city",
    "latitude",
    "longitude",
    "temperature",
    "humidity",
    "wind_speed",
    "rain_probability"
]


# ============================================================
# SAVE WEATHER DATA
# ============================================================

def save_weather_data(
    city,
    latitude,
    longitude,
    weather
):

    logger.info(
        f"Saving weather data for {city}"
    )

    try:

        # ----------------------------------------------------
        # GET CURRENT WEATHER
        # ----------------------------------------------------

        current = weather.get(
            "current",
            {}
        )

        daily = weather.get(
            "daily",
            {}
        )

        # ----------------------------------------------------
        # EXTRACT VALUES
        # ----------------------------------------------------

        temperature = current.get(
            "temperature_2m"
        )

        humidity = current.get(
            "relative_humidity_2m"
        )

        wind_speed = current.get(
            "wind_speed_10m"
        )

        rain_probability = None

        rain_values = daily.get(
            "precipitation_probability_max",
            []
        )

        if rain_values:

            rain_probability = rain_values[0]

        # ----------------------------------------------------
        # CURRENT TIMESTAMP
        # ----------------------------------------------------

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        # ----------------------------------------------------
        # CHECK WHETHER FILE EXISTS
        # ----------------------------------------------------

        file_exists = os.path.exists(
            WEATHER_HISTORY_FILE
        )

        # ----------------------------------------------------
        # WRITE DATA
        # ----------------------------------------------------

        with open(
            WEATHER_HISTORY_FILE,
            "a",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=CSV_HEADERS
            )

            # Write headers only for a new file
            if not file_exists:

                writer.writeheader()

            writer.writerow(
                {
                    "timestamp": timestamp,
                    "city": city,
                    "latitude": latitude,
                    "longitude": longitude,
                    "temperature": temperature,
                    "humidity": humidity,
                    "wind_speed": wind_speed,
                    "rain_probability": rain_probability
                }
            )

        logger.info(
            f"Weather data saved successfully for {city}"
        )

        return True

    except PermissionError as error:

        logger.error(
            f"Permission denied while writing weather data: {error}"
        )

        print(
            "Permission denied while saving weather data."
        )

        return False

    except OSError as error:

        logger.error(
            f"File system error while saving weather data: {error}"
        )

        print(
            "File system error while saving weather data."
        )

        return False

    except Exception as error:

        logger.exception(
            "Unexpected error while saving weather data"
        )

        print(
            "Unexpected storage error:",
            error
        )

        return False


# ============================================================
# READ WEATHER HISTORY
# ============================================================

def read_weather_history():

    logger.info(
        "Reading weather history"
    )

    try:

        if not os.path.exists(
            WEATHER_HISTORY_FILE
        ):

            logger.warning(
                "Weather history file does not exist"
            )

            return []

        with open(
            WEATHER_HISTORY_FILE,
            "r",
            newline="",
            encoding="utf-8"
        ) as file:

            reader = csv.DictReader(
                file
            )

            data = list(reader)

        logger.info(
            f"Weather history loaded successfully: {len(data)} records"
        )

        return data

    except Exception as error:

        logger.exception(
            "Failed to read weather history"
        )

        print(
            "Error reading weather history:",
            error
        )

        return []