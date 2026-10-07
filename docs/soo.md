# Smart Office Sequence of Operations (SOO)

## 1. System Overview & Objectives
The facility utilizes a dual-system mechanical layout managed via BACnet/IP over UDP port 47808[cite: 1]. The primary goal is to maintain occupant thermal comfort while enforcing strict indoor air quality (IAQ) and energy efficiency.

## 2. Operational Modes

### A. Morning Warm-Up / Cool-Down (Occupancy - 2 Hours Prior)
* **Action:** The 5-ton Rooftop Packaged Unit (RTU) initiates a scheduled morning sweep. 
* **Modulation:** VAV dampers are positioned at 50% to accelerate thermal conditioning across the bullpen and conference room zones.

### B. Standard Occupied Operation (08:00 - 18:00)
* **RTU Control:** Supply air temperature is maintained at 55°F via PID loop control based on zone feedback.
* **VAV Modulation:** Individual zone VAV dampers modulate between 20% (minimum airflow) and 100% based on local thermostat temperature error.
* **IDF Infrastructure Cooling:** The dedicated 12,000 BTU mini-split runs continuously[cite: 1], maintaining a strict ambient temperature of 68°F–72°F to prevent server thermal throttling.

### C. IAQ Override & Fresh Air Flush ($CO_2$ Mitigation)
* **Trigger:** The conference room inline $CO_2$ sensor continuously monitors particulate levels[cite: 1]. If concentrations exceed **1,000 ppm** for more than 3 consecutive polling cycles:
  1. The automation core switches `RTU_FreshAir_Flush_Status` to `active`.
  2. The conference room VAV damper overrides thermal logic and locks open to **100%**.
  3. The RTU economizer dampers open fully to purge the zone with outside fresh air.
* **Recovery:** Once $CO_2$ drops below **700 ppm**, the system clears the override flag and returns VAV dampers to standard thermal modulation.

### D. Unoccupied / Night Setback (18:00 - 08:00)
* **Action:** RTU transitions to low-speed fan mode with widened temperature deadbands (62°F heating / 80°F cooling). VAV dampers close to minimum position (10% or fully closed depending on zone requirements).
