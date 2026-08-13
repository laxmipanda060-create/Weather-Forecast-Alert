# 🌦️ Weather Forecast & Alert Application

A Python-based weather monitoring application that retrieves real-time weather information, provides a 7-day forecast, analyzes weather data, and generates alerts for potentially dangerous weather conditions.

This project was developed as a student portfolio project to demonstrate practical skills in:

- Python development
- REST API integration
- Automation
- Data analysis
- Data visualization
- Alert systems
- GUI application development
- Automated testing
- Git and GitHub

---

## 📌 Project Overview

The Weather Forecast & Alert Application connects to public weather services to obtain weather information based on a user's selected city.

The application can:

- Search for a city
- Obtain geographical coordinates
- Retrieve current weather
- Display a 7-day forecast
- Monitor temperature
- Monitor wind speed
- Monitor precipitation probability
- Generate weather alerts
- Store weather history
- Analyze collected weather data
- Display weather information through a GUI
- Run automated tests

The project does not require access to professional weather monitoring hardware or systems.

It uses publicly available weather API services.

---

# ✨ Features

## 🌍 City Search

Users can enter a city name and retrieve its geographical coordinates.

The application uses:

- Latitude
- Longitude
- City name

to obtain weather information.

---

## 🌡️ Current Weather

The application displays current:

- Temperature
- Relative humidity
- Wind speed

---

## 📅 7-Day Forecast

The application retrieves a seven-day weather forecast including:

- Maximum temperature
- Minimum temperature
- Precipitation probability

---

## 🚨 Weather Alert System

The application checks weather conditions against configurable thresholds.

Alerts can be generated for:

- High temperature
- High wind speed
- High precipitation probability

---

## 🔔 Notifications

The application provides notifications when important weather conditions are detected.

---

## 💾 Weather Data Storage

Weather information can be stored locally for historical analysis.

The project uses CSV-based storage for collected weather information.

---

## 📊 Weather Data Analysis

The project includes weather-data analysis using Python and Pandas.

Collected weather information can be used to analyze:

- Temperature
- Humidity
- Wind speed
- Rain probability
- Historical weather records

---

## 📈 Data Visualization

The project uses Python visualization tools to create charts from collected weather information.

---

## 🖥️ Graphical User Interface

The application includes a desktop GUI that allows users to interact with the weather system without using the command line.

---

# 🏗️ Project Architecture

```text
                    ┌──────────────────┐
                    │      User        │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │      GUI         │
                    │    gui.py        │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │   API Layer      │
                    │     api.py       │
                    └────────┬─────────┘
                             │
                             ▼
                 ┌────────────────────────┐
                 │   Public Weather API  │
                 │      Open-Meteo        │
                 └────────────┬───────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │ Weather Response │
                    └────────┬─────────┘
                             │
             ┌───────────────┼────────────────┐
             ▼               ▼                ▼
       ┌──────────┐   ┌─────────────┐   ┌───────────┐
       │ Alerts   │   │ Data Storage│   │ Analysis  │
       └──────────┘   └─────────────┘   └───────────┘
             │               │                │
             ▼               ▼                ▼
       Notifications      CSV Data         Charts