import time

from driver_order import DriverOrder
from driver_config import Authentication, FOOD_BASE_URL

if __name__ == "__main__":
    order = DriverOrder(api_base_url=FOOD_BASE_URL, headers=Authentication.HEADERS)
    while True:
        order.run()
        time.sleep(5)
