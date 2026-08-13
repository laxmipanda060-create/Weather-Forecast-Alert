from winotify import Notification


def send_weather_notification(title, message):

    toast = Notification(
        app_id="Weather Forecast & Alert",
        title=title,
        msg=message
    )

    toast.show()