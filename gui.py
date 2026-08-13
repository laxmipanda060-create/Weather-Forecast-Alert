import tkinter as tk
from tkinter import messagebox, ttk
import subprocess
import sys

from app.api import get_coordinates, get_weather
from app.alerts import check_alerts
from app.storage import save_weather_data
from app.notifications import send_weather_notification
from app.alert_manager import get_new_alerts


# ============================================================
# GLOBAL VARIABLES
# ============================================================

monitoring = False
monitor_job = None


# ============================================================
# GET WEATHER DATA
# ============================================================

def get_weather_data():

    city = city_entry.get().strip()

    if not city:
        messagebox.showwarning(
            "Input Required",
            "Please enter a city name."
        )
        return

    try:

        # ----------------------------------------------------
        # GET CITY COORDINATES
        # ----------------------------------------------------

        location = get_coordinates(city)

        if location is None:
            messagebox.showerror(
                "City Not Found",
                "Could not find the entered city."
            )
            return

        # ----------------------------------------------------
        # GET WEATHER
        # ----------------------------------------------------

        weather = get_weather(
            location["latitude"],
            location["longitude"]
        )

        if weather is None:
            messagebox.showerror(
                "Weather Error",
                "Unable to get weather data."
            )
            return

        # ----------------------------------------------------
        # CURRENT WEATHER
        # ----------------------------------------------------

        current = weather["current"]
        daily = weather["daily"]

        temperature = current["temperature_2m"]
        humidity = current["relative_humidity_2m"]
        wind_speed = current["wind_speed_10m"]

        rain_probability = daily[
            "precipitation_probability_max"
        ][0]

        # ----------------------------------------------------
        # DISPLAY CITY
        # ----------------------------------------------------

        city_result_label.config(
            text=f"📍 {location['name']}"
        )

        # ----------------------------------------------------
        # DISPLAY TEMPERATURE
        # ----------------------------------------------------

        temperature_label.config(
            text=f"🌡️ Temperature: {temperature} °C"
        )

        # ----------------------------------------------------
        # DISPLAY HUMIDITY
        # ----------------------------------------------------

        humidity_label.config(
            text=f"💧 Humidity: {humidity} %"
        )

        # ----------------------------------------------------
        # DISPLAY WIND
        # ----------------------------------------------------

        wind_label.config(
            text=f"💨 Wind Speed: {wind_speed} km/h"
        )

        # ----------------------------------------------------
        # DISPLAY RAIN PROBABILITY
        # ----------------------------------------------------

        rain_label.config(
            text=f"🌧️ Rain Probability: {rain_probability} %"
        )

        # ----------------------------------------------------
        # CHECK WEATHER ALERTS
        # ----------------------------------------------------

        alerts = check_alerts(
            temperature,
            rain_probability,
            wind_speed
        )

        if alerts:

            alert_text = "\n".join(alerts)

            alerts_label.config(
                text=alert_text
            )

            # ------------------------------------------------
            # SMART NOTIFICATION
            # ------------------------------------------------

            new_alerts = get_new_alerts(alerts)

            if new_alerts:

                new_alert_text = "\n".join(
                    new_alerts
                )

                send_weather_notification(
                    "⚠️ Weather Alert",
                    new_alert_text
                )

        else:

            alerts_label.config(
                text="✅ No weather alerts."
            )

            # Reset alert history
            get_new_alerts([])

        # ----------------------------------------------------
        # SAVE WEATHER DATA
        # ----------------------------------------------------

        save_weather_data(
            location["name"],
            location["latitude"],
            location["longitude"],
            weather
        )

        status_label.config(
            text="✅ Weather data saved successfully!"
        )

        # ----------------------------------------------------
        # UPDATE 7-DAY FORECAST
        # ----------------------------------------------------

        update_forecast(daily)

    except Exception as error:

        messagebox.showerror(
            "Application Error",
            f"Something went wrong:\n\n{error}"
        )


# ============================================================
# UPDATE 7-DAY FORECAST
# ============================================================

def update_forecast(daily):

    # Remove old rows
    for item in forecast_table.get_children():
        forecast_table.delete(item)

    dates = daily["time"]

    max_temperatures = daily[
        "temperature_2m_max"
    ]

    min_temperatures = daily[
        "temperature_2m_min"
    ]

    rain_probabilities = daily[
        "precipitation_probability_max"
    ]

    for i in range(len(dates)):

        forecast_table.insert(
            "",
            "end",
            values=(
                dates[i],
                f"{max_temperatures[i]} °C",
                f"{min_temperatures[i]} °C",
                f"{rain_probabilities[i]} %"
            )
        )

# ============================================================
# OPEN ANALYTICS DASHBOARD
# ============================================================

def open_analytics_dashboard():

    try:

        subprocess.Popen(
            [
                sys.executable,
                "dashboard.py"
            ]
        )

    except Exception as error:

        messagebox.showerror(
            "Dashboard Error",
            f"Could not open analytics dashboard.\n\n{error}"
        )
# ============================================================
# START AUTO MONITOR
# ============================================================

def start_monitor():

    global monitoring

    city = city_entry.get().strip()

    if not city:

        messagebox.showwarning(
            "Input Required",
            "Please enter a city name first."
        )

        return

    if monitoring:
        return

    monitoring = True

    monitor_status_label.config(
        text="🔄 Auto monitoring is ON"
    )

    start_monitor_button.config(
        state="disabled"
    )

    stop_monitor_button.config(
        state="normal"
    )

    run_monitor()


# ============================================================
# RUN AUTO MONITOR
# ============================================================

def run_monitor():

    global monitor_job

    if not monitoring:
        return

    get_weather_data()

    selected_interval = interval_var.get()

    if selected_interval == "1 minute":

        minutes = 1

    elif selected_interval == "5 minutes":

        minutes = 5

    elif selected_interval == "10 minutes":

        minutes = 10

    else:

        minutes = 30

    milliseconds = minutes * 60 * 1000

    monitor_status_label.config(
        text=(
            f"🔄 Monitoring ON — "
            f"next check in {minutes} minute(s)"
        )
    )

    monitor_job = window.after(
        milliseconds,
        run_monitor
    )


# ============================================================
# STOP AUTO MONITOR
# ============================================================

def stop_monitor():

    global monitoring
    global monitor_job

    monitoring = False

    if monitor_job is not None:

        try:
            window.after_cancel(monitor_job)

        except Exception:
            pass

        monitor_job = None

    monitor_status_label.config(
        text="⏹️ Auto monitoring is OFF"
    )

    start_monitor_button.config(
        state="normal"
    )

    stop_monitor_button.config(
        state="disabled"
    )


# ============================================================
# MOUSE WHEEL SCROLLING
# ============================================================

def on_mousewheel(event):

    main_canvas.yview_scroll(
        int(-1 * (event.delta / 120)),
        "units"
    )


# ============================================================
# MAIN WINDOW
# ============================================================

window = tk.Tk()

window.title(
    "Weather Forecast & Alert Application"
)

window.geometry(
    "750x750"
)

window.minsize(
    650,
    600
)


# ============================================================
# MAIN SCROLLABLE CANVAS
# ============================================================

main_canvas = tk.Canvas(
    window
)

main_scrollbar = ttk.Scrollbar(
    window,
    orient="vertical",
    command=main_canvas.yview
)

main_canvas.configure(
    yscrollcommand=main_scrollbar.set
)

main_scrollbar.pack(
    side="right",
    fill="y"
)

main_canvas.pack(
    side="left",
    fill="both",
    expand=True
)


# ============================================================
# MAIN CONTENT FRAME
# ============================================================

content_frame = tk.Frame(
    main_canvas
)

canvas_window = main_canvas.create_window(
    (0, 0),
    window=content_frame,
    anchor="nw"
)


# ============================================================
# UPDATE SCROLL REGION
# ============================================================

def configure_scroll_region(event):

    main_canvas.configure(
        scrollregion=main_canvas.bbox("all")
    )


content_frame.bind(
    "<Configure>",
    configure_scroll_region
)


def configure_canvas_width(event):

    main_canvas.itemconfig(
        canvas_window,
        width=event.width
    )


main_canvas.bind(
    "<Configure>",
    configure_canvas_width
)


main_canvas.bind_all(
    "<MouseWheel>",
    on_mousewheel
)


# ============================================================
# TITLE
# ============================================================

title_label = tk.Label(
    content_frame,
    text="🌦️ Weather Forecast & Alert",
    font=("Arial", 24, "bold")
)

title_label.pack(
    pady=(25, 20)
)


# ============================================================
# CITY INPUT
# ============================================================

city_input_label = tk.Label(
    content_frame,
    text="Enter City Name",
    font=("Arial", 13, "bold")
)

city_input_label.pack(
    pady=5
)


city_entry = tk.Entry(
    content_frame,
    font=("Arial", 14),
    width=32
)

city_entry.pack(
    pady=8
)


# ============================================================
# GET WEATHER BUTTON
# ============================================================

weather_button = tk.Button(
    content_frame,
    text="🌤️ Get Weather",
    font=("Arial", 12, "bold"),
    command=get_weather_data
)

weather_button.pack(
    pady=6
)


# ============================================================
# AUTO MONITOR SECTION
# ============================================================

monitor_title = tk.Label(
    content_frame,
    text="⚙️ Automatic Monitoring",
    font=("Arial", 15, "bold")
)

monitor_title.pack(
    pady=(15, 8)
)


interval_label = tk.Label(
    content_frame,
    text="Check weather every:",
    font=("Arial", 11)
)

interval_label.pack(
    pady=3
)


interval_var = tk.StringVar(
    value="1 minute"
)

interval_menu = tk.OptionMenu(
    content_frame,
    interval_var,
    "1 minute",
    "5 minutes",
    "10 minutes",
    "30 minutes"
)

interval_menu.config(
    font=("Arial", 10),
    width=12
)

interval_menu.pack(
    pady=5
)


start_monitor_button = tk.Button(
    content_frame,
    text="🔄 Start Auto Monitor",
    font=("Arial", 11, "bold"),
    command=start_monitor
)

start_monitor_button.pack(
    pady=5
)


stop_monitor_button = tk.Button(
    content_frame,
    text="⏹️ Stop Auto Monitor",
    font=("Arial", 11, "bold"),
    command=stop_monitor,
    state="disabled"
)

stop_monitor_button.pack(
    pady=5
)
# ============================================================
# ANALYTICS DASHBOARD BUTTON
# ============================================================

analytics_button = tk.Button(
    content_frame,
    text="📊 Open Analytics Dashboard",
    font=("Arial", 11, "bold"),
    command=open_analytics_dashboard
)

analytics_button.pack(
    pady=10
)

monitor_status_label = tk.Label(
    content_frame,
    text="Auto monitoring is OFF",
    font=("Arial", 10)
)

monitor_status_label.pack(
    pady=5
)


# ============================================================
# CURRENT WEATHER SECTION
# ============================================================

current_title = tk.Label(
    content_frame,
    text="📊 Current Weather",
    font=("Arial", 17, "bold")
)

current_title.pack(
    pady=(20, 10)
)


city_result_label = tk.Label(
    content_frame,
    text="📍 City",
    font=("Arial", 16, "bold")
)

city_result_label.pack(
    pady=5
)


temperature_label = tk.Label(
    content_frame,
    text="🌡️ Temperature: --",
    font=("Arial", 13)
)

temperature_label.pack(
    pady=3
)


humidity_label = tk.Label(
    content_frame,
    text="💧 Humidity: --",
    font=("Arial", 13)
)

humidity_label.pack(
    pady=3
)


wind_label = tk.Label(
    content_frame,
    text="💨 Wind Speed: --",
    font=("Arial", 13)
)

wind_label.pack(
    pady=3
)


rain_label = tk.Label(
    content_frame,
    text="🌧️ Rain Probability: --",
    font=("Arial", 13)
)

rain_label.pack(
    pady=3
)


# ============================================================
# WEATHER ALERT SECTION
# ============================================================

alerts_title = tk.Label(
    content_frame,
    text="⚠️ Weather Alerts",
    font=("Arial", 17, "bold")
)

alerts_title.pack(
    pady=(20, 8)
)


alerts_label = tk.Label(
    content_frame,
    text="No data yet.",
    font=("Arial", 11),
    wraplength=600,
    justify="center"
)

alerts_label.pack(
    pady=5
)


# ============================================================
# SAVE STATUS
# ============================================================

status_label = tk.Label(
    content_frame,
    text="",
    font=("Arial", 10)
)

status_label.pack(
    pady=8
)


# ============================================================
# 7-DAY FORECAST SECTION
# ============================================================

forecast_title = tk.Label(
    content_frame,
    text="📅 7-Day Weather Forecast",
    font=("Arial", 17, "bold")
)

forecast_title.pack(
    pady=(20, 10)
)


forecast_container = tk.Frame(
    content_frame
)

forecast_container.pack(
    padx=20,
    pady=5,
    fill="x"
)


# ============================================================
# FORECAST TABLE
# ============================================================

columns = (
    "date",
    "max_temp",
    "min_temp",
    "rain"
)

forecast_table = ttk.Treeview(
    forecast_container,
    columns=columns,
    show="headings",
    height=7
)


forecast_table.heading(
    "date",
    text="Date"
)

forecast_table.heading(
    "max_temp",
    text="Max Temperature"
)

forecast_table.heading(
    "min_temp",
    text="Min Temperature"
)

forecast_table.heading(
    "rain",
    text="Rain Probability"
)


forecast_table.column(
    "date",
    width=150,
    anchor="center"
)

forecast_table.column(
    "max_temp",
    width=160,
    anchor="center"
)

forecast_table.column(
    "min_temp",
    width=160,
    anchor="center"
)

forecast_table.column(
    "rain",
    width=160,
    anchor="center"
)


forecast_scrollbar = ttk.Scrollbar(
    forecast_container,
    orient="vertical",
    command=forecast_table.yview
)

forecast_table.configure(
    yscrollcommand=forecast_scrollbar.set
)


forecast_table.pack(
    side="left",
    fill="x",
    expand=True
)

forecast_scrollbar.pack(
    side="right",
    fill="y"
)


# ============================================================
# INFORMATION
# ============================================================

info_label = tk.Label(
    content_frame,
    text=(
        "Weather data is collected using a public weather API.\n"
        "Automatic monitoring stores weather history in CSV format."
    ),
    font=("Arial", 10),
    justify="center"
)

info_label.pack(
    pady=25
)


# ============================================================
# WINDOW CLOSE EVENT
# ============================================================

def close_application():

    stop_monitor()

    window.destroy()


window.protocol(
    "WM_DELETE_WINDOW",
    close_application
)


# ============================================================
# START APPLICATION
# ============================================================

window.mainloop()