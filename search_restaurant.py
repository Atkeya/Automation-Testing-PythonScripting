import requests
import random
import json

class SearchResto:
    def __init__(self, api_base_url, api_base_url_no_user, headers, user_details):
        self.url = api_base_url
        self.url_no_user = api_base_url_no_user
        self.headers = headers
        self.user_details = user_details

    def search_restaurant(self, args):

        url = f"{self.url_no_user}/v404/search/restaurants?exclude_pharma=true&city=1&lon={args['lon']}&page=1&exclude_tong=true&lat={args['lat']}&page_size=10"
        response = requests.get(url, headers=self.headers)
        #print(response.status_code, "restaurant serach")
        if response.status_code == 200:
            return response.json()

        return None

    def get_restaurant_details(self, restaurant_id) -> dict:
        url = f"{self.url}/v202/restaurants/{restaurant_id}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()

        return None

    #     print(f"Restaurant Name is: {response.json()['name']}")
    # if ['accepting_orders'] == 'true' & ['is_open_now'] == 'true' & ['visible_in_app'] == 'true'
    #     print(response)

    def get_items(self, itemid):
        itemid = random.choices['id']
        url = f"{self.url}/"

    def get_random_restaurant(self, restaurants: list) -> str:

        return random.choice(restaurants)

    def validate_restaurant_details(self, details: dict) -> bool:
        # do all validation here, like open now, visible, flags, accepting
        print(f"Restaurant Name is: {details['name']}")
        #print(f"Accepting order = {details['accepting_orders']} | Open Now = {details['is_open_now']} | Visible = {details['visible_in_app']}")
        if details['accepting_orders'] and details['is_open_now'] and details['visible_in_app'] and details['is_resto']==False:
             return True

        return False

    def run(self):
        restaurant_dict = self.search_restaurant({"lat" : self.user_details["latitude"], "lon" : self.user_details["longitude"], "name": 0 , "delivery_fee" : 0})

        if restaurant_dict is not None:
            restaurant_list = restaurant_dict["results"]
            restaurant_ids = []
            for restaurant in restaurant_list:
                resto_id = restaurant["id"]
                restaurant_ids.append(resto_id)

            restaurant_id = self.get_random_restaurant(restaurant_ids)
            print(restaurant_id)

            restaurant_details = self.get_restaurant_details(restaurant_id)

            if restaurant_details is not None and self.validate_restaurant_details(restaurant_details):
                print("Found Open Restaurant, Now finding item")
                return restaurant_details
            else:
                print("Restaurant is not Accepting Order or not open NOW!")

                return None

