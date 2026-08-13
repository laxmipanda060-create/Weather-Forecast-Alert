from app.config import (
    HIGH_TEMPERATURE_THRESHOLD,
    HIGH_WIND_THRESHOLD,
    HIGH_RAIN_PROBABILITY_THRESHOLD
)

from app.logger import logger


# ============================================================
# WEATHER ALERT SYSTEM
# ============================================================

def check_alerts(weather):

    alerts = []

    logger.info(
        "Weather alert checking started"
    )

    try:

        # ----------------------------------------------------
        # GET CURRENT WEATHER
        # ----------------------------------------------------

        current = weather.get(
            "current",
            {}
        )

        # ----------------------------------------------------
        # GET DAILY FORECAST
        # ----------------------------------------------------

        daily = weather.get(
            "daily",
            {}
        )

        # ----------------------------------------------------
        # CURRENT TEMPERATURE
        # ----------------------------------------------------

        temperature = current.get(
            "temperature_2m"
        )

        # ----------------------------------------------------
        # CURRENT WIND SPEED
        # ----------------------------------------------------

        wind_speed = current.get(
            "wind_speed_10m"
        )

        # ----------------------------------------------------
        # RAIN PROBABILITY
        # ----------------------------------------------------

        rain_probability = None

        rain_values = daily.get(
            "precipitation_probability_max",
            []
        )

        if rain_values:

            rain_probability = rain_values[0]

        # ====================================================
        # TEMPERATURE ALERT
        # ====================================================

        if temperature is not None:

            if temperature >= HIGH_TEMPERATURE_THRESHOLD:

                alert_message = (
                    "🔥 HEAT ALERT: "
                    "High temperature detected."
                )

                alerts.append(
                    alert_message
                )

                logger.warning(
                    f"High temperature alert: {temperature}°C"
                )

        # ====================================================
        # WIND ALERT
        # ====================================================

        if wind_speed is not None:

            if wind_speed >= HIGH_WIND_THRESHOLD:

                alert_message = (
                    "💨 WIND ALERT: "
                    "High wind speed detected."
                )

                alerts.append(
                    alert_message
                )

                logger.warning(
                    f"High wind alert: {wind_speed} km/h"
                )

        # ====================================================
        # RAIN ALERT
        # ====================================================

        if rain_probability is not None:

            if (
                rain_probability
                >= HIGH_RAIN_PROBABILITY_THRESHOLD
            ):

                alert_message = (
                    "🌧️ RAIN ALERT: "
                    "High probability of rain."
                )

                alerts.append(
                    alert_message
                )

                logger.warning(
                    "High rain probability detected: "
                    f"{rain_probability}%"
                )

        # ====================================================
        # NO ALERT
        # ====================================================

        if not alerts:

            logger.info(
                "No weather alerts detected"
            )

        else:

            logger.info(
                f"{len(alerts)} weather alert(s) detected"
            )

        return alerts

    except Exception as error:

        logger.exception(
            "Unexpected error while checking weather alerts"
        )

        return [
            "⚠️ Unable to check weather alerts."
        ]