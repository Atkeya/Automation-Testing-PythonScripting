import pprint
import requests
import random


class ITEMCHOICE:

    def __init__(self, api_base_url, api_base_url_no_user, headers, user_details):
        self.url = api_base_url
        self.url_no_user = api_base_url_no_user
        self.headers = headers
        self.user_details = user_details

    def item_list(self, restaurant_id):
        url = f"{self.url}/v202/restaurants/{restaurant_id}/items"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()

        return None

    def get_item_details(self, item_id) -> dict:
        url = f"{self.url_no_user}/v202/items/{item_id}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()

        return None

    def get_random_items(self, items: list, pick) -> list:
        return random.sample(items, k=pick) #used sample same as choices just not to get same id

    def validate_item_details(self, details: dict) -> bool:
        if details['is_available_now'] and details['is_visible'] and details['is_deleted']==False:
             return True

        return False

    def prepare_item_optional_addons(self, item_details):  # adons_list, adon_total_price
        pass

    def prepare_item_required_addons(self, item_details):  # adons_list, adon_total_price
        pass

    def add_adon_item(self, item_details):  # return cart_item, item_total_price
        pass

    def add_non_adon_item(self, item_details): # return cart_item, item_total_price
        print("Found Available Item")
        print(f"Item Name is: {item_details['name']}")

        quantity = random.randint(1, 2)
        price = item_details["price"]
        item_total = quantity * price
        final_item = {
            "id": item_details["id"],
            "addons_optional": [],
            "quantity": quantity,
            "addons_required": []
        }

        pprint.pprint(final_item)
        print("Adding It!")

        return final_item, item_total



    def run(self, restaurant_id): #item khujbo
        cart_items = [] #item storing
        item_total = 0.00
        discounted_item_total = 0.00

        item_list = self.item_list(restaurant_id) #restu dhore item anlam
        if item_list is not None and len(item_list) != 0:
            item_ids = [] #random id stor korar jonno
            items_dict = {} #categoryr bhitor theke item ber kore dict ey nisi
            for category_items in item_list: #catagory looping
                for item in category_items["items"]: #single categoryr items gular looping
                    item_id = item["id"] #item er idr list
                    item_ids.append(item_id)
                    items_dict[item_id] = item #item er details er dict

            how_many_item = min(len(item_ids), 4)
            item_ids = self.get_random_items(item_ids, pick=how_many_item)
            # todo: do in function
            for item_id in item_ids: #item er addon check kore kaaj kora
                item_details = items_dict[item_id] #item dict theke details er check

                # availability er upor check kore validate kora if pass then further process else skip
                if not self.validate_item_details(item_details):
                    continue

                if item_details['has_addon']: #has addon check if yes then 59 line

                    item_super_details = self.get_item_details(item_id)

                    if item_super_details is not None and item_super_details['is_available_now']:
                        print("Found Available Item")
                        print(f"Item Name is: {item_super_details['name']}")
                        item_quantity = random.randint(1, 2)
                        final_price = item_super_details["price"]

                        add_ons_optional = [] #list banaye randomly tule max hobe count porjonto ar min hobe blank
                        final_optional_adons_list = []
                        add_ons_ids_with_price = {}  # key: id => value: adon price
                        for addons_optional in item_super_details['addons_optional']:
                            for item in addons_optional['items']:
                                i_id = item['id']
                                add_ons_optional.append(i_id)
                                add_ons_ids_with_price[i_id] = item['price']

                            if addons_optional['count'] is not None:
                                final_optional_adons_list = self.get_random_items(add_ons_optional, pick=random.randrange(0, addons_optional['count']))
                                for a_id in final_optional_adons_list:
                                    adon_final_price = add_ons_ids_with_price[a_id]
                                    item_total = item_total + (item_quantity * adon_final_price)

                        add_ons_required = [] #randomly tule ocount er soman value dhore rakhbo
                        final_required_adons_list = []
                        add_ons_ids_with_price = {}  # key: id => value: adon price
                        for addons_required in item_super_details['addons_required']:
                            for item in addons_required['items']:
                                i_id = item['id']
                                add_ons_required.append(i_id)
                                add_ons_ids_with_price[i_id] = item['price']

                            if addons_required['count'] is not None:
                                final_required_adons_list = self.get_random_items(add_ons_required, pick=addons_required['count'])
                                for a_id in final_required_adons_list:
                                    adon_final_price = add_ons_ids_with_price[a_id]
                                    item_total = item_total + (item_quantity * adon_final_price)

                        final_item = {
                            "id": item_id,
                            "addons_optional": final_optional_adons_list,
                            "quantity": item_quantity,
                            "addons_required": final_required_adons_list
                        }
                        item_total = item_total + (item_quantity * final_price)

                        cart_items.append(final_item)
                        pprint.pprint(final_item)
                        print("Adding It!")

                else:
                    final_item, total_price = self.add_non_adon_item(item_details)
                    item_total = item_total + total_price
                    cart_items.append(final_item)

        return cart_items, item_total
