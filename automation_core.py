from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Centralized Infrastructure Configuration
# Each zone has a Target (Set Point) and an Actual (Current Env)
zones = {
    "BULLPEN": {"target": 74.0, "actual": 70.0, "unit": "°F"},
    "EXEC_1":  {"target": 72.0, "actual": 72.0, "unit": "°F"},
    "EXEC_2":  {"target": 72.0, "actual": 72.0, "unit": "°F"},
    "CONF_RM": {"target": 450.0, "actual": 500.0, "unit": "PPM"},
    "IDF_CLOSET": {"target": 68.0, "actual": 75.0, "unit": "°F"}
}

def update_simulation():
    for zone in zones:
        t = zones[zone]["target"]
        a = zones[zone]["actual"]
        # Simulation: Gradually close the gap between actual and target
        if a < t: zones[zone]["actual"] += 0.5
        elif a > t: zones[zone]["actual"] -= 0.5

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Update targets based on form input names
        for zone in zones:
            form_val = request.form.get(zone.lower())
            if form_val:
                zones[zone]["target"] = float(form_val)
        return redirect(url_for("index"))
    
    update_simulation()
    return render_template("index.html", zones=zones)
