import requests
import random


class PROMO:

    def __init__(self, api_base_url, headers, user_details):
        self.url = api_base_url
        self.headers = headers
        self.user_details = user_details

    def get_promo_list(self, restaurant_id) -> list:
        url = f"{self.url}/promo-visibility?city_id=101&restaurant_id={restaurant_id}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()

        return []  # for not check None later

    def run(self, restaurant_id) -> dict:
        promos_list = self.get_promo_list(restaurant_id=restaurant_id)
        if len(promos_list) > 0:
            return random.choice(promos_list)
        else:
            print("There are no promo found!")
            return {}
