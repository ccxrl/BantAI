from bleak import BleakScanner, BleakClient
import asyncio

# Replace with your BLE module's MAC address
DEVICE_ADDRESS = " "  # Replace with your BLE module's MAC address
CHARACTERISTIC_UUID = " "  # Replace with the correct characteristic UUID for your module

async def notification_handler(sender, data):
    """Handle incoming data from BLE device."""
    try:
        decoded_data = data.decode().strip()
        print(f"Data received: {decoded_data}")
    except Exception as e:
        print(f"Error decoding data: {e}")

async def main():
    device_address = DEVICE_ADDRESS

    if not device_address:
        print("No address provided. Scanning for devices...")
        devices = await BleakScanner.discover()
        for d in devices:
            print(f"Found device: {d.name} ({d.address})")
            if d.name and ("HC-08" in d.name or "BLE" in d.name):  # Adjust for your device's name
                device_address = d.address
                break

        if not device_address:
            print("Target device not found. Ensure it's powered on and in range.")
            return

    print(f"Attempting to connect to {device_address}...")

    try:
        async with BleakClient(device_address) as client:
            print("Connected!")

            # Subscribe to notifications on the specified characteristic
            await client.start_notify(CHARACTERISTIC_UUID, notification_handler)
            print(f"Subscribed to notifications on {CHARACTERISTIC_UUID}")

            print("Receiving data... Press Ctrl+C to exit.")
            while True:
                await asyncio.sleep(1)  # Keep the connection alive

    except Exception as e:
        print(f"Error: {e}")
    finally:
        print("Disconnected.")

if __name__ == "__main__":
    print("Starting BLE Data Receiver...")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProgram terminated.")
