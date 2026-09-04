import requests
import random
import time
import serial
import logging


# Target URL
url = "https://trial-jk.allbrightlambda.com/gewinn"

def read_serial(port="/dev/ttyUSB0", baudrate=9600):
    try:
        # Open serial connection
        ser = serial.Serial(port, baudrate, timeout=1)
        print(f"Connected to {port} at {baudrate} baud.")
        while True:
            if ser.in_waiting > 0:  # Check if data is available
                print("1")
                data = ser.readline().decode('utf-8', errors='ignore').strip()
                if data:
                    print("2")
                    print(f"Received: {data}")
                    return data

    except serial.SerialException as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("\nStopped by user.")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
        print("Serial connection closed.")

berat = 17


logging.basicConfig(
    filename="/opt/error_record_api.log",   # path to log file
    level=logging.ERROR,             # only log errors and above
    format="%(asctime)s - %(levelname)s - %(message)s"
)





#for i in range(55):
while True:
    try:
        try:
            line = read_serial()
            if line:
                print(f"Received: {line}")
                clean = line.replace('\x02', '').replace('KGM', '').replace('KG','').replace('G','').strip()

                try:
                    berat=int(clean)
                except ValueError:
                    berat = 0
                print(f"berat:{berat}")

        except KeyboardInterrupt:
            print("Stopped by user.")
            berat=0

# Optional query parameters
        params = {
            "device": "jk_oesapa_1",
            "berat": berat
        }

# Optional headers
        headers = {
            "Accept": "application/json"
        }

        try:
    # Send GET request
            response = requests.get(url, params=params, headers=headers)
    
    # Print response details
            print("Status Code:", response.status_code)
            print("params :", params)
            print("Response Body:", response.text)

        except requests.exceptions.RequestException as e:
            print("Error sending GET request:", e)
        time.sleep(1)
    except Exception as e:
        logging.error("An error occurred: %s", e)
        time.sleep(1)  # prevent crash loop

