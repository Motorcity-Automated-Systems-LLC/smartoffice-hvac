# Smart Office Network Architecture & IP Allocation Schema

## Overview
This document outlines the logical network segmentation, layer 2 isolation boundaries (VLANs), and variable-length subnet mask (VLSM) allocations designed for the 2,500 sq. ft. smart office facility.

## Segment Allocations
* **VLAN 10 (Corporate Data):** Allocates a `/28` block providing 14 usable hosts for staff workstations and local peripherals.
* **VLAN 15 (Voice over IP):** Allocates a `/29` block providing 6 usable hosts optimized for priority voice traffic via QoS.
* **VLAN 20 (Building Automation/IoT):** Allocates a `/28` block providing 14 usable host boundaries to secure and isolate BACnet HVAC controllers, Smart TVs, and Smart Whiteboards.

## Core Addressing Table
| VLAN ID | Subnet Function | CIDR Prefix | Network ID | Usable Host Range | Broadcast Address | Gateway Profile |
| :---: | :--- | :---: | :--- | :--- | :--- | :--- |
| 10 | Corporate Data | /28 | 192.168.10.0 | 192.168.10.1 - 192.168.10.14 | 192.168.10.15 | 192.168.10.1 |
| 15 | Voice over IP | /29 | 192.168.10.16 | 192.168.10.17 - 192.168.10.22 | 192.168.10.23 | 192.168.10.17 |
| 20 | Building Automation | /28 | 192.168.10.24 | 192.168.10.25 - 192.168.10.38 | 192.168.10.39 | 192.168.10.25 |

## Physical Topology & MDF Hardware Layout (Layer 1 & 2)
