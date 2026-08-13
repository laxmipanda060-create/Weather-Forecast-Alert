import time
import requests

from app.logger import logger
from app.config import WEATHER_API_URL


# ============================================================
# API RETRY SETTINGS
# ============================================================

MAX_RETRIES = 3

RETRY_DELAY = 2


# ============================================================
# INTERNAL API REQUEST FUNCTION
# ============================================================

def _request_with_retry(
    url,
    params,
    request_name
):
    """
    Send an HTTP GET request with automatic retry handling.

    Retries are performed for:
        - Timeout errors
        - Connection errors
        - HTTP 429
        - HTTP 500
        - HTTP 502
        - HTTP 503
        - HTTP 504
    """

    for attempt in range(1, MAX_RETRIES + 1):

        try:

            logger.info(
                f"{request_name}: "
                f"API request attempt {attempt}/{MAX_RETRIES}"
            )

            response = requests.get(
                url,
                params=params,
                timeout=10
            )

            # ------------------------------------------------
            # SUCCESS
            # ------------------------------------------------

            if response.status_code == 200:

                logger.info(
                    f"{request_name}: "
                    "API request successful"
                )

                return response

            # ------------------------------------------------
            # TEMPORARY SERVER / RATE-LIMIT ERROR
            # ------------------------------------------------

            if response.status_code in (
                429,
                500,
                502,
                503,
                504
            ):

                logger.warning(
                    f"{request_name}: "
                    f"Temporary API error "
                    f"{response.status_code} "
                    f"on attempt {attempt}"
                )

                if attempt < MAX_RETRIES:

                    delay = RETRY_DELAY * attempt

                    logger.info(
                        f"{request_name}: "
                        f"Retrying in {delay} seconds"
                    )

                    time.sleep(delay)

                    continue

                logger.error(
                    f"{request_name}: "
                    "Maximum retry attempts reached"
                )

                return None

            # ------------------------------------------------
            # OTHER HTTP ERROR
            # ------------------------------------------------

            response.raise_for_status()

            return response

        except requests.exceptions.Timeout:

            logger.warning(
                f"{request_name}: "
                f"Request timeout on attempt "
                f"{attempt}/{MAX_RETRIES}"
            )

            if attempt < MAX_RETRIES:

                delay = RETRY_DELAY * attempt

                logger.info(
                    f"{request_name}: "
                    f"Retrying in {delay} seconds"
                )

                time.sleep(delay)

            else:

                logger.error(
                    f"{request_name}: "
                    "Maximum retry attempts reached "
                    "after timeout"
                )

        except requests.exceptions.ConnectionError as error:

            logger.warning(
                f"{request_name}: "
                f"Connection error on attempt "
                f"{attempt}/{MAX_RETRIES}: {error}"
            )

            if attempt < MAX_RETRIES:

                delay = RETRY_DELAY * attempt

                logger.info(
                    f"{request_name}: "
                    f"Retrying in {delay} seconds"
                )

                time.sleep(delay)

            else:

                logger.error(
                    f"{request_name}: "
                    "Maximum retry attempts reached "
                    "after connection error"
                )

        except requests.exceptions.RequestException as error:

            logger.error(
                f"{request_name}: "
                f"API request failed: {error}"
            )

            return None

        except Exception as error:

            logger.exception(
                f"{request_name}: "
                "Unexpected API error"
            )

            return None

    return None


# ============================================================
# GET CITY COORDINATES
# ============================================================

def get_coordinates(city):

    logger.info(
        f"Location search started for city: {city}"
    )

    url = (
        "https://geocoding-api.open-meteo.com/v1/search"
    )

    params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    response = _request_with_retry(
        url,
        params,
        "Location API"
    )

    if response is None:

        print(
            "Unable to connect to the location service."
        )

        return None

    try:

        data = response.json()

        if "results" not in data:

            logger.warning(
                f"City not found: {city}"
            )

            print(
                f"City '{city}' was not found."
            )

            return None

        if not data["results"]:

            logger.warning(
                f"No location results found for: {city}"
            )

            print(
                f"City '{city}' was not found."
            )

            return None

        location = data["results"][0]

        city_name = location.get(
            "name",
            city
        )

        latitude = location.get(
            "latitude"
        )

        longitude = location.get(
            "longitude"
        )

        logger.info(
            f"Location found successfully: {city_name}"
        )

        return {
            "name": city_name,
            "latitude": latitude,
            "longitude": longitude
        }

    except ValueError as error:

        logger.error(
            f"Invalid location API JSON response: {error}"
        )

        print(
            "Invalid response received from location service."
        )

        return None

    except Exception as error:

        logger.exception(
            "Unexpected error while processing coordinates"
        )

        print(
            "Unexpected location error:",
            error
        )

        return None


# ============================================================
# GET WEATHER DATA
# ============================================================

def get_weather(latitude, longitude):

    logger.info(
        "Weather API request started"
    )

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "wind_speed_10m"
        ),
        "daily": (
            "temperature_2m_max,"
            "temperature_2m_min,"
            "precipitation_probability_max"
        ),
        "forecast_days": 7,
        "timezone": "auto"
    }

    response = _request_with_retry(
        WEATHER_API_URL,
        params,
        "Weather API"
    )

    if response is None:

        print(
            "Weather service is temporarily unavailable."
        )

        logger.error(
            "Weather API request failed after retries"
        )

        return None

    try:

        weather_data = response.json()

        logger.info(
            "Weather API response received successfully"
        )

        # ----------------------------------------------------
        # BASIC RESPONSE VALIDATION
        # ----------------------------------------------------

        if "current" not in weather_data:

            logger.error(
                "Weather API response does not contain "
                "current weather data"
            )

            print(
                "Invalid weather data received from API."
            )

            return None

        if "daily" not in weather_data:

            logger.warning(
                "Weather API response does not contain "
                "daily forecast data"
            )

        logger.info(
            "Weather JSON data parsed successfully"
        )

        return weather_data

    except ValueError as error:

        logger.error(
            f"Invalid weather API JSON response: {error}"
        )

        print(
            "Invalid response received from weather service."
        )

        return None

    except Exception as error:

        logger.exception(
            "Unexpected error while processing weather data"
        )

        print(
            "Unexpected weather processing error:",
            error
        )

        return None