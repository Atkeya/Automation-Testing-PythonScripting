import requests
import time
import json

from driver_config import Authentication

# (for forward dispatch)active food location ping: "get food-1"
# (for single order dispatch)supply ping: get me-one"

DRIVER_PING_BASE_URL = "https://locations.example-stageenv.xyz"


class DriverPing:
    def __init__(self, api_base_url, headers):
        self.url = api_base_url
        self.headers = headers

    @staticmethod
    def display_result(ref, res, expected_code=200):
        if res.status_code == expected_code:
            print(f"{ref} -> success")
        else:
            print(f"{ref} -> ", res.content)

    def ping(self):
        url = f"{self.url}/v101/batch"
        current_time = int(time.time())
        elapsed_threshold = 153  # range(140, 199)
        gps_time = current_time - elapsed_threshold

        payload = {
            "batch_location_pings": [
                {
                    "accuracy": "9.269",
                    "bearing": "0.0",
                    "current_altitude": 00.0000,
                    "current_latitude": 00.0000,
                    "current_longitude": 00.0000,
                    "device_time": current_time,
                    "elapsed_location_age": elapsed_threshold,
                    "gps_timestamp": gps_time,
                    "is_mock": False,
                    "speed": "0.02231451"
                }
            ],
            "battery_level": 81,
            "device_id": "6e-774/28e25\8cc4b1dr1v1r",
            "device_name": "samsung SM-M536B",
            "is_open_for_deliveries": True,
            "is_running_foreground": True,
            "location_mode": 3,
            "os_version": "11"
        }

        response = requests.post(url, headers=self.headers, data=json.dumps(payload))
        self.display_result("Ping", response)


if __name__ == "__main__":
    counter = 0
    dp = DriverPing(api_base_url=DRIVER_PING_BASE_URL, headers=Authentication.HEADERS)

    while True:
        dp.ping()
        counter += 1
        time.sleep(5)
        print(f"Ping count: {counter}")
