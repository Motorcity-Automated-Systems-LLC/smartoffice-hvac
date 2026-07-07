# Mechanical HVAC Zoning & BACnet Point List

## System Layout
* **Primary System:** 5-Ton Rooftop Unit (RTU) handling common zones via independent Variable Air Volume (VAV) branches.
* **Secondary System:** Dedicated 12,000 BTU Ductless Mini-Split system managing the IDF Server Closet 24/7/365.

## Data Point Register (Layer 7 Object Map)
| Device Identifier | Object/Point Name | Native Data Type | Scale/Units | Description |
| :--- | :--- | :--- | :--- | :--- |
| VAV-01 (Bullpen) | `BULLPEN_ZONE_TEMP` | Analog Input | °F | Main open office area air temp |
| VAV-01 (Damper) | `BULLPEN_DAMPER_POS` | Analog Output | 0 - 100 % | Modulates open air volume airflow |
| VAV-02 (Conf Rm) | `CONF_RM_CO2_LEVEL`| Analog Input | PPM | Indoor air quality monitor |
| VAV-02 (Damper) | `CONF_DAMPER_POS`   | Analog Output | 0 - 100 % | Fresh air ventilation intake |
| MS-01 (IDF Closet)| `IDF_CLOSET_TEMP`   | Analog Input | °F | Server room structural load temp |
| MS-01 (Safety)   | `IDF_ALARM_STATUS`  | Binary Input | 0=OK / 1=ALARM| High-limit thermal threshold trip |
