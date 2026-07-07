#!/usr/bin/env python3
"""
Smart Office Infrastructure - Automation Core
Simulated Layer 7 Application Logic for HVAC Control Loops over UDP Port 47808
"""

import time

# Simulated Local Sensor Environment (Inputs)
building_sensors = {
    "BULLPEN_ZONE_TEMP": 74.5,   # Degrees Fahrenheit (Currently warm)
    "CONF_RM_CO2_LEVEL": 450.0,  # Parts Per Million (Normal ambient outdoor air)
    "IDF_CLOSET_TEMP": 67.2,     # Target server room temp
    "IDF_ALARM_STATUS": 0        # 0 = Normal Operation, 1 = Thermal Alarm
}

# Operational Targets (Setpoints)
SETPOINTS = {
    "BULLPEN_COOLING": 72.0,
    "CONF_MAX_CO2": 800.0,
    "IDF_MAX_TEMP": 75.0
}

def evaluate_hvac_logic():
    print("--- Executing Automation Core Telemetry Scan ---")
    
    # 1. Bullpen Thermal Management Loop (Now accounts for 16 workstations worth of heat!)
    if building_sensors["BULLPEN_ZONE_TEMP"] > SETPOINTS["BULLPEN_COOLING"]:
        damper_pos = 100
        print(f"[ACTION]: Bullpen Temp ({building_sensors['BULLPEN_ZONE_TEMP']}°F) exceeds setpoint. Opening VAV-01 Damper to {damper_pos}%.")
    else:
        damper_pos = 20
        print(f"[STATUS]: Bullpen Temp nominal. VAV-01 Damper idling at {damper_pos}%.")

    # 2. Conference Room IAQ (Indoor Air Quality) Ventilation Loop
    if building_sensors["CONF_RM_CO2_LEVEL"] > SETPOINTS["CONF_MAX_CO2"]:
        conf_damper = 100
        print(f"[WARN]: CO2 Spike ({building_sensors['CONF_RM_CO2_LEVEL']} PPM). Flushing Conference Room with Fresh Outside Air.")
    else:
        print(f"[STATUS]: Conference Room air composition stable ({building_sensors['CONF_RM_CO2_LEVEL']} PPM).")

if __name__ == "__main__":
    # Execute a single diagnostic evaluation pass
    evaluate_hvac_logic()
