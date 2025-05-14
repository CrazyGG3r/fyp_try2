import serial
import time

# Replace with your ESP32 Bluetooth COM port (Check in Device Manager on Windows or `ls /dev/` on Linux/Mac)
ESP32_PORT = "COM7"  # Example for Windows
# ESP32_PORT = "/dev/ttyUSB0"  # Example for Linux/Mac

BAUD_RATE = 115200

try:
    # Open serial connection
    esp32 = serial.Serial(ESP32_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)  # Wait for connection to establish

    while True:
        command = input("Enter command (LED ON / LED OFF / EXIT): ").strip()
        if command.lower() == "exit":
            print("Exiting...")
            break

        esp32.write((command + "\n").encode())  # Send command
        time.sleep(1)  # Wait for response

        # Read response from ESP32
        while esp32.in_waiting:
            print("ESP32:", esp32.readline().decode().strip())

except serial.SerialException:
    print("Could not connect to ESP32. Check COM port.")

finally:
    if 'esp32' in locals():
        esp32.close()
