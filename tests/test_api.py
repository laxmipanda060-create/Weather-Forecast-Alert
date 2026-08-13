import requests

from app import api


# ============================================================
# TEST CITY COORDINATES - SUCCESS
# ============================================================

def test_get_coordinates_success(monkeypatch):

    class FakeResponse:

        status_code = 200

        def raise_for_status(self):
            pass

        def json(self):

            return {
                "results": [
                    {
                        "name": "Berhampur",
                        "latitude": 19.315,
                        "longitude": 84.798
                    }
                ]
            }

    def fake_get(*args, **kwargs):
        return FakeResponse()

    monkeypatch.setattr(
        requests,
        "get",
        fake_get
    )

    result = api.get_coordinates(
        "Berhampur"
    )

    assert result is not None
    assert result["name"] == "Berhampur"
    assert result["latitude"] == 19.315
    assert result["longitude"] == 84.798


# ============================================================
# TEST CITY NOT FOUND
# ============================================================

def test_get_coordinates_city_not_found(monkeypatch):

    class FakeResponse:

        status_code = 200

        def raise_for_status(self):
            pass

        def json(self):

            return {
                "results": []
            }

    def fake_get(*args, **kwargs):
        return FakeResponse()

    monkeypatch.setattr(
        requests,
        "get",
        fake_get
    )

    result = api.get_coordinates(
        "UnknownCity"
    )

    assert result is None


# ============================================================
# TEST WEATHER API - SUCCESS
# ============================================================

def test_get_weather_success(monkeypatch):

    class FakeResponse:

        status_code = 200

        def raise_for_status(self):
            pass

        def json(self):

            return {
                "current": {
                    "temperature_2m": 28.5,
                    "relative_humidity_2m": 80,
                    "wind_speed_10m": 12
                },

                "daily": {
                    "temperature_2m_max": [30],
                    "temperature_2m_min": [25],
                    "precipitation_probability_max": [70]
                }
            }

    def fake_get(*args, **kwargs):
        return FakeResponse()

    monkeypatch.setattr(
        requests,
        "get",
        fake_get
    )

    result = api.get_weather(
        19.315,
        84.798
    )

    assert result is not None
    assert "current" in result
    assert "daily" in result

    assert (
        result["current"]["temperature_2m"]
        == 28.5
    )


# ============================================================
# TEST WEATHER API - TIMEOUT
# ============================================================

def test_get_weather_failure(monkeypatch):

    def fake_get(*args, **kwargs):

        raise requests.exceptions.Timeout(
            "Connection timed out"
        )

    monkeypatch.setattr(
        requests,
        "get",
        fake_get
    )

    result = api.get_weather(
        19.315,
        84.798
    )

    assert result is None