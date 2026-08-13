# ============================================================
# SMART ALERT MANAGER
# ============================================================

last_alerts = set()


def should_notify(alerts):
    """
    Decide whether a desktop notification should be sent.

    A notification is sent only when a new alert appears.
    """

    global last_alerts

    current_alerts = set(alerts)

    # No alerts
    if not current_alerts:

        last_alerts = set()

        return False

    # Check whether there is a new alert
    new_alerts = current_alerts - last_alerts

    # Update stored alerts
    last_alerts = current_alerts

    # Return True only for new alerts
    return len(new_alerts) > 0


def get_new_alerts(alerts):
    """
    Return only alerts that have not been notified yet.
    """

    global last_alerts

    current_alerts = set(alerts)

    new_alerts = current_alerts - last_alerts

    last_alerts = current_alerts

    return list(new_alerts)


def reset_alerts():
    """
    Reset the alert history.
    """

    global last_alerts

    last_alerts = set()