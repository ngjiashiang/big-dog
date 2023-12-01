import requests
import time
import os

url = "http://10.5.51.188/api/robot"

# Function to send the POST request
def send_post_request():
    try:
        # Use os.popen to execute the command and capture its output
        temperature_command = "vcgencmd measure_temp"
        raw_temperature = os.popen(temperature_command).read().strip()

        # Extract the numeric part of the temperature string
        cpu_temperature = raw_temperature.replace("temp=", "").replace("'C", "")

        payload = {
            "id": 4,
            "private_key": "CoSXhiVyz6XRygLLwfd8",
            "current_task": "monitoring cpu temp",
            "data": cpu_temperature,
        }

        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        print(f"POST request successful: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending POST request: {e}")

# Main loop to send the POST request every 10 seconds
while True:
    send_post_request()
    time.sleep(10)
