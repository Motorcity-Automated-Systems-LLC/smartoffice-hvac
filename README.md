# Smart Office Infrastructure & Automation Core
A comprehensive engineering project designing a secure, high-efficiency smart facility from the ground up. This repository bridges the gap between Layer 1-4 IT network architecture and Layer 7 Industrial Building Automation Systems (BAS).

## 🏢 Project Scope & Floor Plan
![Office Floor Plan](docs/smartoffice-3d.png)

The target environment is a modern 2,500 sq. ft. commercial office space optimized for efficient resource usage, operational isolation, and high-security boundaries. 

The physical environment consists of:
* **The Main Bullpen:** Two modular workspace clusters containing a total of 16 open-concept desk workstations, a centralized multi-function printer, a smart TV, and an interactive digital whiteboard.
* **The Conference Room:** Central meeting space equipped with a VoIP conference phone, smart TV, and collaboration whiteboard.
* **Executive Offices:** Two private office spaces with dedicated computing terminals and VoIP desk endpoints.
* **The IDF Closet:** A secure, climate-controlled core room housing the main server rack, firewall appliance, managed switches, and primary automation engine controls.

---

## ❄️ Mechanical HVAC Architecture & Sequence of Operations
To account for varied thermal and occupational loads across distinct structural zones, the facility utilizes a dual-system mechanical layout managed over **BACnet/IP over UDP Port 47808**:

1. **Common Space Multi-Zone System:** A 5-ton commercial Rooftop Packaged Unit (RTU) supplying air volume to individual zones via specialized **Variable Air Volume (VAV) branches**.
    * *Occupancy-Driven Ventilation:* The Conference Room VAV branch incorporates an inline $CO_2$ sensor. When occupancy thresholds exceed 1,000 ppm, the automation core overrides thermal logic to flush the zone with outside fresh air.
2. **Critical Infrastructure Cooling:** A dedicated, ductless 12,000 BTU Mini-Split heat pump operating 24/7/365 inside the IDF Closet to prevent equipment thermal throttling.

*Detailed operating rules and control loops are documented in the [Sequence of Operations (`docs/soo.md`)](docs/soo.md).*  
*Detailed object mapping can be found in the [HVAC Point List Database (`docs/hvac_points.md`)](docs/hvac_points.md).*

---

## 🌐 Network Segmentation & Subnetting Strategy
To eliminate security vulnerabilities and maximize network performance, the infrastructure discards flat networking models in favor of strict **Layer 2 VLAN isolation** and **Variable Length Subnet Masking (VLSM)** utilizing the private `192.168.10.0` address space:

* **VLAN 10 | Corporate Data (`192.168.10.0/27`):** Expands to a `/27` block providing 30 usable host addresses to comfortably accommodate the 16 bullpen computers, private offices, and local peripheral expansion.
* **VLAN 15 | Voice Over IP (`192.168.10.32/29`):** Isolates time-sensitive voice traffic into a tight 6-host pool to enforce Quality of Service (QoS) priorities and eliminate packet jitter.
* **VLAN 20 | Building Automation System (`192.168.10.40/28`):** Encloses BACnet controllers, IoT Smart TVs, and smart whiteboards in a firewalled 14-usable host industrial segment completely blocked from external public routing vectors.

*Detailed network schematics, switch configs, and firewall ACL rules can be found in the [Network Architecture & Topology Schema (`docs/network_topology.md`)](docs/network_topology.md).*

---

## 📊 Observability & Telemetry Pipeline
The repository features a fully closed-loop software stack. The asynchronous Python automation core (`src/automation_core.py`) evaluates control logic and simultaneously streams live time-series telemetry data into a local **InfluxDB 2.7** instance, which is visualized in real-time through **Grafana OSS**.

---

## 📁 Repository Directory Structure
```text
smart-office-infrastructure/
│
├── .github/
│   └── workflows/
│       └── validate.yml          <-- CI/CD pipeline for code linting and doc integrity
│
├── docs/
│   ├── blueprints/               <-- Architectural floor plan renders[cite: 1]
│   ├── hvac_points.md            <-- BACnet object parameters & point inventories
│   ├── network_topology.md       <-- Subnet tables, VLAN profiles, & MDF port mappings[cite: 2]
│   └── soo.md                    <-- Sequence of Operations technical control logic
│
├── network_configs/
│   ├── switch_config.ios         <-- Cisco IOS-XE switch port profiles & VLAN trunking
│   └── firewall_rules.acl        <-- Zero-trust inter-VLAN firewall access control lists
│
├── src/
│   └── automation_core.py        <-- Python BACpypes3 engine with InfluxDB telemetry bridge
│
└── docker-compose.yml            <-- Local observability stack (InfluxDB + Grafana)
