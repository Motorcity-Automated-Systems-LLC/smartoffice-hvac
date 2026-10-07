# HVAC Point List Database (BACnet/IP)

## Overview
This document defines the complete BACnet object point inventory for the 2,500 sq. ft. smart office facility. All points communicate via **BACnet/IP over UDP Port 47808** within the isolated **VLAN 20 (Building Automation / IoT)** network segment.

Objects are categorized by mechanical system and controller assignment, utilizing standard BACnet object types (AI: Analog Input, AO: Analog Output, BI: Binary Input, BO: Binary Output, AV: Analog Value, BV: Binary Value).

---

## 1. Common Space: 5-Ton Rooftop Packaged Unit (RTU-1) Points

| Object Identifier | Point Name / Tag | Type | Description / Function | Units / State Text |
| :--- | :--- | :---: | :--- | :--- |
| `AI:101` | `RTU1_Supply_Temp` | AI | Supply air temperature leaving the RTU heat exchanger | °F |
| `AI:102` | `RTU1_Return_Temp` | AI | Common space return air temperature header | °F |
| `AI:103` | `RTU1_Outside_Air_Temp` | AI | Ambient outside air temperature (OAT) for economizer logic | °F |
| `AO:101` | `RTU1_Supply_Fan_Speed` | AO | Supply fan variable frequency drive (VFD) output command | % (0–100%) |
| `AO:102` | `RTU1_Economizer_Damper` | AO | Outside air economizer damper modulation position | % (0–100%) |
| `BI:101` | `RTU1_Fan_Status` | BI | Differential pressure switch proving fan operation | Inactive (Off) / Active (Running) |
| `BO:101` | `RTU1_Compressor_Cmd` | BO | Stage 1/2 mechanical cooling compressor enable command | Inactive (Off) / Active (Running) |
| `BV:101` | `RTU1_FreshAir_Flush_Status` | BV | Global override flag indicating active IAQ outside air purge | Inactive / Active |

---

## 2. Conference Room: VAV Branch & IAQ Points

| Object Identifier | Point Name / Tag | Type | Description / Function | Units / State Text |
| :--- | :--- | :---: | :--- | :--- |
| `AI:201` | `ConfRoom_Temp` | AI | Actual zone temperature in the conference room | °F |
| `AI:202` | `ConfRoom_CO2_PPM` | AI | Inline carbon dioxide particulate sensor for occupancy IAQ | ppm (400–2000+) |
| `AO:201` | `ConfRoom_VAV_Damper` | AO | VAV terminal unit damper actuator position command | % (20% Min - 100% Max) |
| `AV:201` | `ConfRoom_Temp_Setpoint` | AV | Active user-defined thermal setpoint for conference space | °F (Default: 72°F) |
| `BI:201` | `ConfRoom_Occupancy_PIR` | BI | Passive Infrared (PIR) motion sensor detecting zone presence | Inactive (Vacant) / Active (Occupied) |

---

## 3. IDF Closet: Critical Infrastructure Cooling (Mini-Split) Points

| Object Identifier | Point Name / Tag | Type | Description / Function | Units / State Text |
| :--- | :--- | :---: | :--- | :--- |
| `AI:301` | `IDF_Ambient_Temp` | AI | Ambient server room temperature monitored at rack intake | °F |
| `AI:302` | `IDF_Humidity` | AI | Relative humidity sensor inside the secure core room | % RH |
| `AO:301` | `IDF_MiniSplit_Setpoint` | AO | Dedicated 12,000 BTU ductless heat pump temperature target | °F (Default: 70°F) |
| `BI:301` | `IDF_MiniSplit_Fault_Status`| BI | Compressor or condensate overflow fault alarm monitor | Normal (OK) / Fault (Alarm) |
| `BO:301` | `IDF_MiniSplit_Power_Cmd` | BO | Hard override command to cycle backup mini-split cooling | Inactive (Off) / Active (On) |

---

## 4. System-Wide Global & Virtual Objects (`automation_core.py`)

| Object Identifier | Point Name / Tag | Type | Description / Function | Units / State Text |
| :--- | :--- | :---: | :--- | :--- |
| `AV:901` | `Facility_Mode_State` | AV | System operating state: 0=Unoccupied, 1=Warmup, 2=Occupied, 3=IAQ Flush | Enum Code (0–3) |
| `BV:901` | `Global_Fire_Interlock` | BV | Emergency fire alarm shutdown trigger interlock | Normal / Tripped (Shutdown) |
