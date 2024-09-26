import time
import requests
import json


class DriverOrder:

    def __init__(self, api_base_url, headers):
        self.url = api_base_url
        self.headers = headers

    def run(self):
        self.patch_order()

    @staticmethod
    def get_req_body(file_path):
        contents = {}
        with open(file_path, "r") as file:
            contents = file.read()

        return contents

    @staticmethod
    def display_result(ref, res, expected_code=200):
        if res.status_code == expected_code:
            print(f"{ref} -> success")
        else:
            print(f"{ref} -> ", res.content)

    def get_open_orders(self):
        orders = []
        url = f"{self.url}/v505/orders/open?&lat=00.0000&lng=00.0000"
        response = requests.get(url, headers=self.headers)
        # self.display_result("open order", response)

        if response.status_code == 200:
            orders = response.json()
            print(f"Order count: {len(orders)}")

        return orders

    def give_rating(self, order_id):
        url = f"{self.url}/rating"
        payload = {"order": order_id, "rating": 1}
        response = requests.post(url, headers=self.headers, data=json.dumps(payload))
        print("Order has been Completed")

    def patch_order(self):
        orders = self.get_open_orders()
        if len(orders) > 0:
            # loop through orders and get order status
            for order in orders:
                desire_status = ""

                # check status
                if order['status'] == "ASSIGNED":
                    desire_status = "ACCEPTED"
                elif order['status'] == "ACCEPTED":
                    desire_status = "PLACED"
                elif order['status'] == "PLACED":
                    desire_status = "PICKED_UP"
                elif order['status'] == "PICKED_UP":
                    desire_status = "DELIVERED"
                elif order['status'] == "DELIVERED":
                    self.give_rating(order['id'])
                else:
                    continue

                url = f"{self.url}/v202/orders/{order['id']}"
                payload = {
                    "accepted_lat": 00.0000,
                    "accepted_lon": 00.0000,
                    "status": desire_status
                }

                if desire_status == "":
                    payload = {"driver_pay_status": 1}
                    url = f"{self.url}/v303/orders/{order['id']}"
                    desire_status = "paid"

                response = requests.patch(url, headers=self.headers, data=json.dumps(payload))
                self.display_result(f"order status updated to {desire_status}:", response)

                time.sleep(5)

        else:
            print("no order found!")
