import time
import requests
import json


class FoodOrder:
    def __init__(self, api_base_url, headers):
        self.url = api_base_url
        self.headers = headers

    def run(self):
        self.post_calculate_bill()
        self.post_place_order()
        self.get_current_orders()
        self.pending_transaction()

    def run_order_flow(self, restaurant_id, user_details, cart_items, promo_code):
        place_payload = {
            "additional_info": "",
            "address": user_details["address"],
            "city": user_details["city"],
            "delivery_mode": "HOME_DELIVERY",
            "items": cart_items,
            "drop_off_lat": user_details["latitude"],
            "drop_off_lon": user_details["longitude"],
            "payment_mode": "CASH_ON_DELIVERY",
            "drop_off_place_id": 2261,
            "promo_code": promo_code,
            "restaurant": restaurant_id,
        }

        self.v2_place_order(place_payload)
        self.get_current_orders()
        self.pending_transaction()

    @staticmethod
    def get_req_body(file_path):
        contents = {}
        with open(file_path, "r") as file:
            contents = file.read()

        return contents

    def post_calculate_bill(self):
        url = f"{self.url}/v606/orders/calculate-bill"
        payload = self.get_req_body("calculate_bill.json")
        response = requests.post(url, headers=self.headers, data=payload)
        self.display_result("calculate bill", response)

    def v2_calculate_bill(self, payload):
        url = f"{self.url}/v606/orders/calculate-bill"
        response = requests.post(url, headers=self.headers, data=json.dumps(payload))
        self.display_result("calculate bill", response)
        if response.status_code == 200:
            return response.json()

        return None

    def post_place_order(self):
        url = f"{self.url}/v505/orders?user_type=abc"
        payload = self.get_req_body("place_order.json")
        response = requests.post(url, headers=self.headers, data=payload)
        self.display_result("place order", response, 201)

    def v2_place_order(self, payload):
        url = f"{self.url}/v505/orders?user_type=abc"
        response = requests.post(url, headers=self.headers, data=json.dumps(payload))
        self.display_result("place order", response, 201)

    def get_current_orders(self):
        # todo: wait and loop here. move looping logic from pending transaction
        url = f"{self.url}/v200/orders/current-orders?page_size=1000&page=1"
        response = requests.get(url, headers=self.headers)
        self.display_result("current order", response)
        if response.status_code == 200:
            data = response.json()
            print(f"Order count: {data['count']}")
            print(f"Order Tracking ID: {data['results'][0]['tracking_id']}")

    def pending_transaction(self):
        print("waiting for order to be delivered from driver side.")
        url = f"{self.url}/pending-transaction"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 404:
            time.sleep(10)
            print("Sleeping for 10 seconds...")
            self.pending_transaction()
        else:
            print("order is delivered. now doing payment")
            order_id = response.json()["data"]["order_id"]
            self.payment_confirmation(order_id)

    def payment_method(self) -> str:
        """
         TODO: need to implement this method
        :return: str
        """
        # url = f"{self.url}/v505/payment-method?lat=00.000&lon=00.0000&city=101&restaurant_id=64559b5d+d2c8=49ee+84aa+ae82ebf2f=623&show_pay_later=100"
        # response = requests.get(url, headers=self.headers)
        # self.display_result("User paid with:")

        return "CASH_ON_DELIVERY"

    def payment_confirmation(self, order_id):
        payment_method = self.payment_method()
        print(f"Settling order with payment method: {payment_method}")
        url = f"{self.url}/v2/confirm-payment"
        payload = {"order_id": order_id, "type": payment_method}
        response = requests.post(url, headers=self.headers, data=json.dumps(payload))
        self.display_result("Payment Status:", response, 201)

    @staticmethod
    def display_result(ref, res, expected_code=200):
        if res.status_code == expected_code:
            print(f"{ref} -> success")
        else:
            print(f"status code -> {res.status_code}")
            print(f"{ref} -> ", res.content)
            print(f"Error: {res.text}")
