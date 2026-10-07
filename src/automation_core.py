"""
Smart Office Automation Core - BACnet/IP Simulation & InfluxDB Telemetry Bridge
Simulates polling HVAC points, evaluating CO2 thresholds, triggering damper overrides,
and streaming time-series data to InfluxDB.
"""

import asyncio
import logging
import os
from bacpypes3.argparse import SimpleArgumentParser
from bacpypes3.app import Application
from bacpypes3.local.analog import AnalogValueObject
from bacpypes3.local.binary import BinaryValueObject

# InfluxDB Client Imports
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# Configure logging
logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)

class SmartOfficeAutomationCore:
    def __init__(self, address: str):
        self.app = Application(address)
        
        # Initialize InfluxDB Client (Connecting to local Docker container)
        self.influx_url = os.getenv("INFLUX_URL", "http://localhost:8086")
        self.influx_token = os.getenv("INFLUX_TOKEN", "adminpassword")
        self.influx_org = os.getenv("INFLUX_ORG", "motorcity-automation")
        self.influx_bucket = os.getenv("INFLUX_BUCKET", "facility-telemetry")

        try:
            self.influx_client = InfluxDBClient(
                url=self.influx_url, 
                token=self.influx_token, 
                org=self.influx_org
            )
            self.write_api = self.influx_client.write_api(write_options=SYNCHRONOUS)
            _logger.info(f"Connected to InfluxDB at {self.influx_url}")
        except Exception as e:
            _logger.error(f"Failed to connect to InfluxDB: {e}")
            self.write_api = None

        # Initialize Virtual BACnet Objects based on README & Point Lists
        self.co2_sensor = AnalogValueObject(
            objectIdentifier=("analogValue", 1),
            objectName="ConfRoom_CO2_PPM",
            presentValue=450.0,
            units="partsPerMillion"
        )
        self.app.add_object(self.co2_sensor)

        self.vav_damper = AnalogValueObject(
            objectIdentifier=("analogValue", 2),
            objectName="ConfRoom_VAV_Damper",
            presentValue=30.0,
            units="percent"
        )
        self.app.add_object(self.vav_damper)

        self.flush_override = BinaryValueObject(
            objectIdentifier=("binaryValue", 1),
            objectName="RTU_FreshAir_Flush_Status",
            presentValue="inactive"
        )
        self.app.add_object(self.flush_override)

    def push_to_influx(self, co2: float, damper: float, status: str):
        """Pushes current telemetry metrics to InfluxDB time-series database."""
        if not self.write_api:
            return
        
        try:
            point = (
                Point("facility_metrics")
                .tag("zone", "conference_room")
                .tag("system", "rtu_vav")
                .float_field("co2_ppm", co2)
                .float_field("vav_damper_pct", damper)
                .string_field("flush_status", status)
            )
            self.write_api.write(bucket=self.influx_bucket, org=self.influx_org, record=point)
        except Exception as e:
            _logger.error(f"Error writing telemetry to InfluxDB: {e}")

    async def control_loop(self):
        """Main control loop running every 5 seconds to poll, log, and stream data."""
        _logger.info("Starting Smart Office BACnet Automation Loop & Telemetry Bridge...")
        
        CO2_WARNING_THRESHOLD = 1000.0  # ppm
        CO2_RECOVERY_THRESHOLD = 700.0  # ppm

        try:
            while True:
                current_co2 = self.co2_sensor.presentValue
                current_damper = self.vav_damper.presentValue
                current_status = self.flush_override.presentValue

                _logger.info(
                    f"Polling Telemetry -> CO2: {current_co2} ppm | "
                    f"VAV Damper: {current_damper}% | "
                    f"Flush Mode: {current_status}"
                )

                # Sequence of Operations: CO2 Occupancy Overrides
                if current_co2 >= CO2_WARNING_THRESHOLD and current_status == "inactive":
                    _logger.warning(
                        f"HIGH CO2 DETECTED ({current_co2} ppm). Overriding RTU and VAV damper for fresh air flush!"
                    )
                    self.flush_override.presentValue = "active"
                    self.vav_damper.presentValue = 100.0
                    
                elif current_co2 <= CO2_RECOVERY_THRESHOLD and current_status == "active":
                    _logger.info(
                        f"CO2 levels recovered ({current_co2} ppm). Reverting to standard thermal control."
                    )
                    self.flush_override.presentValue = "inactive"
                    self.vav_damper.presentValue = 30.0

                # Stream current states into InfluxDB
                self.push_to_influx(
                    self.co2_sensor.presentValue, 
                    self.vav_damper.presentValue, 
                    self.flush_override.presentValue
                )

                await asyncio.sleep(5)

        except asyncio.CancelledError:
            _logger.info("Automation control loop stopped.")

async def main():
    parser = SimpleArgumentParser()
    args = parser.parse_args()
    
    controller = SmartOfficeAutomationCore(args.ini.address)
    loop_task = asyncio.create_task(controller.control_loop())
    
    try:
        await asyncio.Future()
    finally:
        loop_task.cancel()
        await loop_task

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        _logger.info("Shutting down automation core gracefully.")
