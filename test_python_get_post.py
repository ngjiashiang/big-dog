import requests
import json
import time

CHARGE_FLAG_MAP = {
    1: "Not charging",
    2: "Charging with charging pile",
    3: "Charging with adapter",
    8: "Connecting to charging pile"
}

EMERGENCY_BUTTON_MAP = {
    0: "Engaged",
    1: "Disengaged"
}

NAVIGATION_STATUS_MAP = {
    0: "Not navigating",
    3: "Success",
    4: "Failed"
}


# Function to get data from the first endpoint
def get_base_encode_data():
    url = "http://192.168.10.2/reeman/base_encode"
    response = requests.get(url)
    return response.json()

# Function to get data from the second endpoint
def get_movebase_status():
    url = "http://192.168.10.2/reeman/movebase_status"
    response = requests.get(url)
    return response.json()

# Function to send a POST request to the target API
def send_post_request(battery_level, current_task, error_code, data_field):
    url = "http://10.5.51.188/api/robot"
    payload = {
        "id": 4,
        "private_key": "m03SIH3grIQGTWOwXmtl",
        "current_task": current_task,
        "error_code": error_code,
        "data": json.dumps(data_field),  # Convert data to JSON string
        "battery_level": battery_level  # Use battery level from the previous get request
    }
    response = requests.post(url, json=payload)
    print("POST Request Status Code:", response.status_code)

# Main loop
while True:
    try:
        # Get data from the first endpoint
        base_encode_data = get_base_encode_data()

        # Get data from the second endpoint
        movebase_status = get_movebase_status()

        # Prepare data for the POST request
        data_field = {
            "Charge flag": CHARGE_FLAG_MAP.get(base_encode_data.get("chargeFlag", 0), "Unknown"),
            "Emergency button": EMERGENCY_BUTTON_MAP.get(base_encode_data.get("emergencyButton", 0), "Unknown"),
            "Navigation status": NAVIGATION_STATUS_MAP.get(movebase_status.get("status", 0), "Unknown")
        }

        # Send POST request
        send_post_request(
            base_encode_data.get("battery", 0),
            "Jia Shiang hasent gave me any task",
            " ",
            data_field
        )

    except Exception as e:
        print("An error occurred:", e)
        # Handle the error if needed
    time.sleep(10)