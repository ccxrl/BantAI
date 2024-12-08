from bleak import BleakScanner, BleakClient
import asyncio

#BT04-A address 02:11:22:33:AC:B3
# Define your CGB-1165 MAC address here 98:DA:60:08:01:82
CGB_1165_ADDRESS = "98:DA:60:08:01:82"  

async def notification_handler(sender, data):
    """Handle incoming data from BLE device"""
    try:
        # Decode bytes to string
        decoded_data = data.decode().strip()
        print(f"Received Data: {decoded_data}")

        # Extract BPM and Avg BPM from the string
        if "BPM=" in decoded_data:
            bpm_data = decoded_data.split(",")  # Split into parts
            bpm = float(bpm_data[0].split("=")[1])  # Extract BPM value
            avg_bpm = float(bpm_data[1].split("=")[1])  # Extract Avg BPM value
            print(f"Heart Rate: {bpm} BPM, Average Heart Rate: {avg_bpm} BPM")
    except Exception as e:
        print(f"Error processing data: {e}")


async def main():
    device_address = CGB_1165_ADDRESS

    if not device_address:
        print("No address provided. Scanning for BT04-A...")
        devices = await BleakScanner.discover()
        for d in devices:
            print(f"Found device: {d.name} ({d.address})")
            if d.name and ("CGB-1165" in d.name or "MLT-BT05" in d.name):
                print(f"Found BT04-A device at address: {d.address}")
                device_address = d.address
                break

        if not device_address:
            print("BT04-A device not found. Please ensure it's powered on and in range.")
            return

    print(f"Attempting to connect to {device_address}...")

    try:
        async with BleakClient(device_address) as client:
            print("Connected!")

            # Get all services
            services = await client.get_services()
            
            # Find the characteristic we want to subscribe to
            for service in services:
                for char in service.characteristics:
                    if "notify" in char.properties:
                        # Subscribe to notifications
                        await client.start_notify(char.uuid, notification_handler)
                        print(f"Subscribed to notifications on {char.uuid}")
            
            # Keep the connection alive
            while True:
                await asyncio.sleep(1)
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("Starting BLE Heart Rate Monitor...")
    asyncio.run(main())
