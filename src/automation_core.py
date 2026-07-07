#!/usr/bin/env python3
from flask import Flask, render_template, request, redirect, url_for
import os

# This tells Flask to look for the 'templates' folder inside the 'src' directory
app = Flask(__name__, template_folder='templates')

# Live Global State (Simulated BACnet Instance Memory)
building_sensors = {
    "BULLPEN_ZONE_TEMP": 74.5,
    "CONF_RM_CO2_LEVEL": 450.0,
    "IDF_CLOSET_TEMP": 67.2
}

SETPOINTS = {
    "BULLPEN_COOLING": 72.0,
    "CONF_MAX_CO2": 800.0,
    "IDF_MAX_TEMP": 75.0
}

@app.route("/")
def index():
    # Pass our current live stats over to our visual HTML layout
    return render_template("index.html", data=building_sensors)

@app.route("/update", methods=["POST"])
def update_telemetry():
    # Capture input values from the dashboard sliders
    building_sensors["BULLPEN_ZONE_TEMP"] = float(request.form.get("bullpen_temp"))
    building_sensors["CONF_RM_CO2_LEVEL"] = float(request.form.get("conf_co2"))
    building_sensors["IDF_CLOSET_TEMP"] = float(request.form.get("idf_temp"))
    
    # Process the engineering control logic loops based on new inputs
    execute_bms_logic()
    
    return redirect(url_for("index"))

def execute_bms_logic():
    print("\n--- RUNNING BACKEND HVAC BOUNDARY EVALUATION ---")
    
    # 1. Bullpen Variable Air Volume Check
    if building_sensors["BULLPEN_ZONE_TEMP"] > SETPOINTS["BULLPEN_COOLING"]:
        print(f"[ACTION]: Bullpen Temp ({building_sensors['BULLPEN_ZONE_TEMP']}°F) high. Opening VAV-01 Damper to 100%.")
    else:
        print(f"[STATUS]: Bullpen operating within nominal thermal thresholds.")

    # 2. Conference Room Fresh Air Flush Check
    if building_sensors["CONF_RM_CO2_LEVEL"] > SETPOINTS["CONF_MAX_CO2"]:
        print(f"[WARN]: CO2 Spike ({building_sensors['CONF_RM_CO2_LEVEL']} PPM). Modulating fresh air intake loop.")
    else:
        print(f"[STATUS]: Conference room air exchange rates stable.")

if __name__ == "__main__":
    # Bind to environment port or default to standard local test port
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
