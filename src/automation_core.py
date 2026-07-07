#!/usr/bin/env python3
from flask import Flask, render_template, request, redirect, url_for
import os
import json

# Absolute path setup for cloud environments (Render/Heroku/etc)
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__, template_folder=os.path.join(basedir, 'templates'))
DATA_FILE = os.path.join(basedir, "data_store.json")

# Default startup values
DEFAULT_DATA = {
    "BULLPEN_ZONE_TEMP": 74.5,
    "CONF_RM_CO2_LEVEL": 450.0,
    "IDF_CLOSET_TEMP": 67.2,
    "OFFICE_1_TEMP": 72.0,
    "OFFICE_2_TEMP": 72.0,
    "NETWORK_STATUS": "OPERATIONAL"
}

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f: return json.load(f)
        except: return DEFAULT_DATA
    return DEFAULT_DATA

def save_data(data):
    with open(DATA_FILE, "w") as f: json.dump(data, f)

@app.route("/")
def index():
    return render_template("index.html", data=load_data())

@app.route("/update", methods=["POST"])
def update_telemetry():
    # Capture all form inputs
    data = {
        "BULLPEN_ZONE_TEMP": float(request.form.get("bullpen_temp")),
        "CONF_RM_CO2_LEVEL": float(request.form.get("conf_co2")),
        "IDF_CLOSET_TEMP": float(request.form.get("idf_temp")),
        "OFFICE_1_TEMP": float(request.form.get("office_1_temp")),
        "OFFICE_2_TEMP": float(request.form.get("office_2_temp")),
        "NETWORK_STATUS": "OPERATIONAL"
    }
    
    save_data(data)
    execute_bms_logic(data)
    return redirect(url_for("index"))

def execute_bms_logic(data):
    # This simulates the control loops (The "PLC" brain of your BAS)
    print("\n--- BAS AUTOMATION ENGINE ACTIVE ---")
    if data["BULLPEN_ZONE_TEMP"] > 72.0:
        print("[ACTION]: VAV-01 Damper modulated to 100% for Bullpen cooling.")
    if data["CONF_RM_CO2_LEVEL"] > 800.0:
        print("[WARN]: High occupancy detected. Increasing fresh air intake.")

if __name__ == "__main__":
    # Render assigns the PORT automatically; default to 5000 for local test
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
