from app.alerts import check_alerts
from app.config import (
    HIGH_TEMPERATURE_THRESHOLD,
    HIGH_WIND_THRESHOLD,
    HIGH_RAIN_PROBABILITY_THRESHOLD
)


# ============================================================
# TEST 1 - NO ALERT
# ============================================================

def test_no_weather_alert():

    temperature = 25
    rain_probability = 20
    wind_speed = 10

    alerts = check_alerts(
        temperature,
        rain_probability,
        wind_speed
    )

    assert alerts == []


# ============================================================
# TEST 2 - HIGH TEMPERATURE
# ============================================================

def test_high_temperature_alert():

    temperature = (
        HIGH_TEMPERATURE_THRESHOLD + 5
    )

    rain_probability = 20
    wind_speed = 10

    alerts = check_alerts(
        temperature,
        rain_probability,
        wind_speed
    )

    assert len(alerts) >= 1

    assert any(
        "HEAT ALERT" in alert
        for alert in alerts
    )


# ============================================================
# TEST 3 - HIGH WIND
# ============================================================

def test_high_wind_alert():

    temperature = 25
    rain_probability = 20

    wind_speed = (
        HIGH_WIND_THRESHOLD + 10
    )

    alerts = check_alerts(
        temperature,
        rain_probability,
        wind_speed
    )

    assert len(alerts) >= 1

    assert any(
        "WIND ALERT" in alert
        for alert in alerts
    )


# ============================================================
# TEST 4 - HIGH RAIN
# ============================================================

def test_high_rain_alert():

    temperature = 25

    rain_probability = (
        HIGH_RAIN_PROBABILITY_THRESHOLD + 10
    )

    wind_speed = 10

    alerts = check_alerts(
        temperature,
        rain_probability,
        wind_speed
    )

    assert len(alerts) >= 1

    assert any(
        "RAIN ALERT" in alert
        for alert in alerts
    )


# ============================================================
# TEST 5 - MULTIPLE ALERTS
# ============================================================

def test_multiple_weather_alerts():

    temperature = (
        HIGH_TEMPERATURE_THRESHOLD + 5
    )

    rain_probability = (
        HIGH_RAIN_PROBABILITY_THRESHOLD + 10
    )

    wind_speed = (
        HIGH_WIND_THRESHOLD + 10
    )

    alerts = check_alerts(
        temperature,
        rain_probability,
        wind_speed
    )

    assert len(alerts) == 3