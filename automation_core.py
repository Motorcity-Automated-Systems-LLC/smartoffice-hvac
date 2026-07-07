from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# This is your "Source of Truth." 
# Any key added here is available to the entire app.
config = {
    "BULLPEN_ZONE_TEMP": 74.0,
    "CONF_RM_CO2_LEVEL": 450.0,
    "IDF_CLOSET_TEMP": 68.0,
    "OFFICE_1_TEMP": 72.0,
    "OFFICE_2_TEMP": 72.0
}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # We update the 'config' dictionary directly using the names from index.html
        config["BULLPEN_ZONE_TEMP"] = float(request.form.get("bullpen_temp"))
        config["CONF_RM_CO2_LEVEL"] = float(request.form.get("conf_co2"))
        config["IDF_CLOSET_TEMP"] = float(request.form.get("idf_temp"))
        config["OFFICE_1_TEMP"] = float(request.form.get("office_1_temp"))
        config["OFFICE_2_TEMP"] = float(request.form.get("office_2_temp"))
        return redirect(url_for("index"))
    
    return render_template("index.html", data=config)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
