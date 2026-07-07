#!/usr/bin/env python3
from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__, template_folder='templates')

# The "Running Configuration" of your BAS/Network
# This represents the state of your infrastructure
config = {
    "BULLPEN_TEMP": 74.0, "CONF_CO2": 450, "IDF_TEMP": 68.0,
    "OFFICE_1_TEMP": 72.0, "OFFICE_2_TEMP": 72.0,
    "VLAN_10_STATUS": "ACTIVE", "VLAN_20_STATUS": "ACTIVE"
}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Update the running config
        config["BULLPEN_TEMP"] = float(request.form.get("bullpen_temp"))
        config["CONF_CO2"] = float(request.form.get("conf_co2"))
        config["IDF_TEMP"] = float(request.form.get("idf_temp"))
        config["OFFICE_1_TEMP"] = float(request.form.get("office_1_temp"))
        config["OFFICE_2_TEMP"] = float(request.form.get("office_2_temp"))
        return redirect(url_for("index"))
    
    return render_template("index.html", data=config)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
