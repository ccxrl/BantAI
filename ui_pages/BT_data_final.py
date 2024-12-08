from bleak import BleakScanner, BleakClient
import asyncio
import keyboard
import signal
import sys

CGB_1165_ADDRESS = "98:DA:60:08:01:82"

# Global flag to control the main loop
running = True


async def notification_handler(sender, data):
    """Handle incoming data from BLE device"""
    try:
        # Decode bytes to string
        decoded_data = data.decode().strip()

        # Check for "No finger detected" message
        if "No finger detected" in decoded_data:
            print("\nNo finger detected - Please place finger on sensor")
            return

        # Extract BPM and Avg BPM from the string
        if "BPM=" in decoded_data:
            bpm_data = decoded_data.split(",")  # Split into parts
            bpm = float(bpm_data[0].split("=")[1])  # Extract BPM value
            avg_bpm = float(bpm_data[1].split("=")[1])  # Extract Avg BPM value
            print(f"Heart Rate: {bpm} BPM, Average Heart Rate: {avg_bpm} BPM")
    except ValueError as ve:
        # Handle the case where we can't convert the values to float
        # This might happen during transition states
        pass
    except Exception as e:
        print(f"Error processing data: {e}")


def handle_exit():
    """Handle program exit gracefully"""
    global running
    running = False
    print("\nStopping BLE connection...")


async def main():
    global running
    device_address = CGB_1165_ADDRESS

    # Setup keyboard event listener
    keyboard.on_press_key('x', lambda _: handle_exit())

    if not device_address:
        print("No address provided. Scanning for BCGB-1165..")
        devices = await BleakScanner.discover()
        for d in devices:
            print(f"Found device: {d.name} ({d.address})")
            if d.name and ("CGB-1165" in d.name or "BT04-A" in d.name):
                print(f"Found BLE device at address: {d.address}")
                device_address = d.address
                break

        if not device_address:
            print("CGB-1165 device not found. Please ensure it's powered on and in range.")
            return

    print(f"Attempting to connect to {device_address}...")
    print("Press 'x' to stop the program...")

    try:
        async with BleakClient(device_address) as client:
            print("Connected!")
            print("Place your finger on the sensor to begin readings...")

            # Get all services
            services = await client.get_services()

            # Find the characteristic we want to subscribe to
            for service in services:
                for char in service.characteristics:
                    if "notify" in char.properties:
                        # Subscribe to notifications
                        await client.start_notify(char.uuid, notification_handler)
                        print(f"Subscribed to notifications on {char.uuid}")

            # Keep the connection alive until 'x' is pressed
            while running:
                await asyncio.sleep(0.1)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        print("BLE connection terminated.")


if __name__ == "__main__":
    print("Starting BLE Heart Rate Monitor...")
    print("Press 'x' to stop at any time...")

    # Handle Ctrl+C as well
    signal.signal(signal.SIGINT, lambda x, y: handle_exit())

    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Program terminated: {e}")
    finally:
        # Cleanup
        keyboard.unhook_all()