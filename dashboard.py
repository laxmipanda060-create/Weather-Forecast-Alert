import tkinter as tk
from tkinter import ttk, messagebox

import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# ============================================================
# LOAD DATA
# ============================================================

FILE_PATH = "data/weather_history.csv"


def load_data():

    try:

        df = pd.read_csv(FILE_PATH)

        if "timestamp" in df.columns:
            df["timestamp"] = pd.to_datetime(
                df["timestamp"],
                errors="coerce"
            )

        return df

    except FileNotFoundError:

        messagebox.showerror(
            "Data File Missing",
            f"Could not find:\n{FILE_PATH}"
        )

        return pd.DataFrame()

    except Exception as error:

        messagebox.showerror(
            "Data Error",
            str(error)
        )

        return pd.DataFrame()


# ============================================================
# MAIN WINDOW
# ============================================================

window = tk.Tk()

window.title(
    "Weather Analytics Dashboard"
)

window.geometry(
    "1200x750"
)

window.minsize(
    950,
    650
)


# ============================================================
# TITLE
# ============================================================

title_label = tk.Label(
    window,
    text="📊 Weather Analytics Dashboard",
    font=("Arial", 24, "bold")
)

title_label.pack(
    pady=(15, 5)
)


subtitle_label = tk.Label(
    window,
    text="Historical Weather Data Analysis",
    font=("Arial", 11)
)

subtitle_label.pack(
    pady=(0, 15)
)


# ============================================================
# LOAD DATA
# ============================================================

df = load_data()

if df.empty:

    window.mainloop()
    raise SystemExit


# ============================================================
# STATISTICS FRAME
# ============================================================

stats_frame = tk.Frame(
    window
)

stats_frame.pack(
    fill="x",
    padx=20,
    pady=10
)


# ============================================================
# HELPER FUNCTION FOR STAT CARDS
# ============================================================

def create_stat_card(
    parent,
    title,
    value,
    column
):

    frame = tk.Frame(
        parent,
        relief="ridge",
        borderwidth=2,
        padx=20,
        pady=10
    )

    frame.grid(
        row=0,
        column=column,
        padx=8,
        sticky="nsew"
    )

    title = tk.Label(
        frame,
        text=title,
        font=("Arial", 10, "bold")
    )

    title.pack()

    value_label = tk.Label(
        frame,
        text=value,
        font=("Arial", 18, "bold")
    )

    value_label.pack(
        pady=(5, 0)
    )

    return frame


# ============================================================
# CALCULATE STATISTICS
# ============================================================

record_count = len(df)

if "temperature" in df.columns:

    avg_temp = df["temperature"].mean()
    max_temp = df["temperature"].max()
    min_temp = df["temperature"].min()

else:

    avg_temp = 0
    max_temp = 0
    min_temp = 0


# ============================================================
# STAT CARDS
# ============================================================

stats_frame.columnconfigure(
    0,
    weight=1
)

stats_frame.columnconfigure(
    1,
    weight=1
)

stats_frame.columnconfigure(
    2,
    weight=1
)

stats_frame.columnconfigure(
    3,
    weight=1
)


create_stat_card(
    stats_frame,
    "Total Records",
    str(record_count),
    0
)


create_stat_card(
    stats_frame,
    "Average Temperature",
    f"{avg_temp:.1f} °C",
    1
)


create_stat_card(
    stats_frame,
    "Maximum Temperature",
    f"{max_temp:.1f} °C",
    2
)


create_stat_card(
    stats_frame,
    "Minimum Temperature",
    f"{min_temp:.1f} °C",
    3
)


# ============================================================
# CHART NOTEBOOK
# ============================================================

notebook = ttk.Notebook(
    window
)

notebook.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=10
)


# ============================================================
# TEMPERATURE TAB
# ============================================================

temperature_frame = tk.Frame(
    notebook
)

notebook.add(
    temperature_frame,
    text="🌡️ Temperature"
)


if (
    "timestamp" in df.columns
    and "temperature" in df.columns
):

    figure1 = Figure(
        figsize=(9, 5),
        dpi=100
    )

    axis1 = figure1.add_subplot(
        111
    )

    axis1.plot(
        df["timestamp"],
        df["temperature"],
        marker="o"
    )

    axis1.set_title(
        "Temperature History"
    )

    axis1.set_xlabel(
        "Time"
    )

    axis1.set_ylabel(
        "Temperature (°C)"
    )

    axis1.tick_params(
        axis="x",
        rotation=30
    )

    figure1.tight_layout()

    canvas1 = FigureCanvasTkAgg(
        figure1,
        master=temperature_frame
    )

    canvas1.draw()

    canvas1.get_tk_widget().pack(
        fill="both",
        expand=True
    )


# ============================================================
# HUMIDITY TAB
# ============================================================

humidity_frame = tk.Frame(
    notebook
)

notebook.add(
    humidity_frame,
    text="💧 Humidity"
)


if (
    "timestamp" in df.columns
    and "humidity" in df.columns
):

    figure2 = Figure(
        figsize=(9, 5),
        dpi=100
    )

    axis2 = figure2.add_subplot(
        111
    )

    axis2.plot(
        df["timestamp"],
        df["humidity"],
        marker="o"
    )

    axis2.set_title(
        "Humidity History"
    )

    axis2.set_xlabel(
        "Time"
    )

    axis2.set_ylabel(
        "Humidity (%)"
    )

    axis2.tick_params(
        axis="x",
        rotation=30
    )

    figure2.tight_layout()

    canvas2 = FigureCanvasTkAgg(
        figure2,
        master=humidity_frame
    )

    canvas2.draw()

    canvas2.get_tk_widget().pack(
        fill="both",
        expand=True
    )


# ============================================================
# WIND TAB
# ============================================================

wind_frame = tk.Frame(
    notebook
)

notebook.add(
    wind_frame,
    text="💨 Wind"
)


if (
    "timestamp" in df.columns
    and "wind_speed" in df.columns
):

    figure3 = Figure(
        figsize=(9, 5),
        dpi=100
    )

    axis3 = figure3.add_subplot(
        111
    )

    axis3.plot(
        df["timestamp"],
        df["wind_speed"],
        marker="o"
    )

    axis3.set_title(
        "Wind Speed History"
    )

    axis3.set_xlabel(
        "Time"
    )

    axis3.set_ylabel(
        "Wind Speed (km/h)"
    )

    axis3.tick_params(
        axis="x",
        rotation=30
    )

    figure3.tight_layout()

    canvas3 = FigureCanvasTkAgg(
        figure3,
        master=wind_frame
    )

    canvas3.draw()

    canvas3.get_tk_widget().pack(
        fill="both",
        expand=True
    )


# ============================================================
# RAIN TAB
# ============================================================

rain_frame = tk.Frame(
    notebook
)

notebook.add(
    rain_frame,
    text="🌧️ Rain"
)


if (
    "timestamp" in df.columns
    and "rain_probability" in df.columns
):

    figure4 = Figure(
        figsize=(9, 5),
        dpi=100
    )

    axis4 = figure4.add_subplot(
        111
    )

    axis4.plot(
        df["timestamp"],
        df["rain_probability"],
        marker="o"
    )

    axis4.set_title(
        "Rain Probability History"
    )

    axis4.set_xlabel(
        "Time"
    )

    axis4.set_ylabel(
        "Rain Probability (%)"
    )

    axis4.tick_params(
        axis="x",
        rotation=30
    )

    figure4.tight_layout()

    canvas4 = FigureCanvasTkAgg(
        figure4,
        master=rain_frame
    )

    canvas4.draw()

    canvas4.get_tk_widget().pack(
        fill="both",
        expand=True
    )


# ============================================================
# CLOSE APPLICATION
# ============================================================

def close_dashboard():

    window.destroy()


window.protocol(
    "WM_DELETE_WINDOW",
    close_dashboard
)


# ============================================================
# START DASHBOARD
# ============================================================

window.mainloop()