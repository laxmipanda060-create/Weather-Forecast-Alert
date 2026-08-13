import logging
import os


# ============================================================
# LOG DIRECTORY
# ============================================================

LOG_DIRECTORY = "logs"

os.makedirs(
    LOG_DIRECTORY,
    exist_ok=True
)


# ============================================================
# LOG FILE
# ============================================================

LOG_FILE = os.path.join(
    LOG_DIRECTORY,
    "weather_app.log"
)


# ============================================================
# LOGGER CONFIGURATION
# ============================================================

logging.basicConfig(
    level=logging.INFO,

    format=(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(name)s | "
        "%(message)s"
    ),

    handlers=[
        logging.FileHandler(
            LOG_FILE,
            encoding="utf-8"
        ),

        logging.StreamHandler()
    ]
)


# ============================================================
# APPLICATION LOGGER
# ============================================================

logger = logging.getLogger(
    "WeatherApplication"
)