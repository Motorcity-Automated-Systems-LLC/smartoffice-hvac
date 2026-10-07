"""
Smart Office Automation Core - BACnet/IP Simulation Engine
Simulates polling HVAC points, evaluating CO2 thresholds, and triggering damper overrides.
"""

import asyncio
import logging
from bacpypes3.argparse import SimpleArgumentParser
from bacpypes3.app import Application
from bacpypes3.local.analog import AnalogValueObject
from bacpypes3.local.binary import BinaryValueObject
from bacpypes3.pdu import GlobalBroadcast

# Configure logging
logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)

class SmartOfficeAutomationCore:
    def __init__(self, address: str):
        self.app = Application(address)
        
        # Initialize Virtual BACnet Objects based on README & Point Lists
        # 1. Conference Room CO2 Sensor (ppm) - Normal baseline ~400ppm
        self.co2_sensor = AnalogValueObject(
            objectIdentifier=("analogValue", 1),
            objectName="ConfRoom_CO2_PPM",
            presentValue=450.0,
            units="partsPerMillion"
        )
        self.app.add_object(self.co2_sensor)

        # 2. Conference Room VAV Damper Position (%)
        self.vav_damper = AnalogValueObject(
            objectIdentifier=("analogValue", 2),
            objectName="ConfRoom_VAV_Damper",
            presentValue=30.0,
            units="percent"
        )
        self.app.add_object(self.vav_damper)

        # 3. RTU Fresh Air Flush Override (Binary: Active/Inactive)
        self.flush_override = BinaryValueObject(
            objectIdentifier=("binaryValue", 1),
            objectName="RTU_FreshAir_Flush_Status",
            presentValue="inactive"
        )
        self.app.add_object(self.flush_override)

    async def control_loop(self):
        """Main control loop running every 5 seconds to poll and trigger logic."""
        _logger.info("Starting Smart Office BACnet Automation Loop...")
        
        # Threshold constants
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
                    self.vav_damper.presentValue = 100.0  # Open VAV to max position
                    
                elif current_co2 <= CO2_RECOVERY_THRESHOLD and current_status == "active":
                    _logger.info(
                        f"CO2 levels recovered ({current_co2} ppm). Reverting to standard thermal control."
                    )
                    self.flush_override.presentValue = "inactive"
                    self.vav_damper.presentValue = 30.0  # Return to baseline modulation

                await asyncio.sleep(5)

        except asyncio.CancelledError:
            _logger.info("Automation control loop stopped.")

async def main():
    parser = SimpleArgumentParser()
    args = parser.parse_args()
    
    # Initialize application bound to local VLAN 20 interface address
    controller = SmartOfficeAutomationCore(args.ini.address)
    
    # Start the background control loop alongside the BACnet service
    loop_task = asyncio.create_task(controller.control_loop())
    
    try:
        await asyncio.Future()  # Run forever
    finally:
        loop_task.cancel()
        await loop_task

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        _logger.info("Shutting down automation core gracefully.")
