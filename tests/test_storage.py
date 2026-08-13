import csv

from app import storage


# ============================================================
# SAMPLE WEATHER DATA
# ============================================================

SAMPLE_WEATHER = {

    "current": {
        "temperature_2m": 28.5,
        "relative_humidity_2m": 80,
        "wind_speed_10m": 12
    },

    "daily": {
        "precipitation_probability_max": [
            70
        ]
    }
}


# ============================================================
# TEST WEATHER DATA STORAGE
# ============================================================

def test_save_weather_data(
    tmp_path,
    monkeypatch
):

    test_file = (
        tmp_path /
        "weather_history.csv"
    )

    monkeypatch.setattr(
        storage,
        "WEATHER_HISTORY_FILE",
        str(test_file)
    )

    result = storage.save_weather_data(
        city="Berhampur",
        latitude=19.315,
        longitude=84.798,
        weather=SAMPLE_WEATHER
    )

    assert result is True

    assert test_file.exists()

    with open(
        test_file,
        "r",
        newline="",
        encoding="utf-8"
    ) as file:

        rows = list(
            csv.DictReader(file)
        )

    assert len(rows) == 1

    assert rows[0]["city"] == "Berhampur"

    assert (
        rows[0]["temperature"]
        == "28.5"
    )

    assert (
        rows[0]["humidity"]
        == "80"
    )

    assert (
        rows[0]["wind_speed"]
        == "12"
    )

    assert (
        rows[0]["rain_probability"]
        == "70"
    )


# ============================================================
# TEST WEATHER HISTORY WHEN FILE DOES NOT EXIST
# ============================================================

def test_read_empty_weather_history(
    tmp_path,
    monkeypatch
):

    test_file = (
        tmp_path /
        "missing_weather_history.csv"
    )

    monkeypatch.setattr(
        storage,
        "WEATHER_HISTORY_FILE",
        str(test_file)
    )

    result = (
        storage.read_weather_history()
    )

    assert result == []