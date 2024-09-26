from food_order import FoodOrder
import pprint

#take addons: final_price
#take item:final_price
#item price: item_id + add_ons id theke niye quantity diye calculate korbo
#subtotal: item_price+vat+SC kore calculate korbo
#Total_Bill: subtotal + delivery charge + promo(if any) + Restaurant Discount(if any) kore calculate korbo


class CalculateBillAssertion:
    def __init__(self, api_base_url, headers, user_details):
        self.url = api_base_url
        self.headers = headers
        self.user_details = user_details

    def run_calculate_bill_flow(self, restaurant_details, cart_items, item_total, promo_code) -> bool:
        payload = {
            "city": 101,
            "items": cart_items,
            "drop_off_lat": self.user_details["latitude"],
            "drop_off_lon": self.user_details["longitude"],
            "promo_code": promo_code,
            "restaurant": restaurant_details['id']
        }
        order = FoodOrder(api_base_url=self.url, headers=self.headers)
        data = order.v2_calculate_bill(payload)
        if data is not None:
            self.assertion(data, restaurant_details, item_total, promo_code)
            return True, data['is_promo_applied']

        return False, None

    def assertion(self, data: dict, restaurant_details, item_total, promo_code):
        # check item total
        item_total = round(item_total, 2)
        api_item_total = data["bill"]["item_price"]
        print(item_total, "<- Item Total ->", api_item_total)
        assert item_total == api_item_total, "item total doesn't match!"

        # check vat
        vat = 0.0
        vat_percentage = restaurant_details["vat"]
        if vat_percentage > 0:
            vat = item_total*(vat_percentage/100.00)

        api_vat = data["bill"]["vat"]
        print(vat, "<- Vat ->", api_vat)
        assert vat == api_vat, "vat doesn't match!"

        # check restaurant service charge
        sc = 0.0
        sc_percentage = restaurant_details["service_charge"]
        if sc_percentage > 0:
            sc = item_total * (sc_percentage / 100.00)

        api_sc = data["bill"]["service_charge"]
        print(sc, "<- Service_Charge ->", api_sc)
        assert sc == api_sc, "service charge doesn't match!"

        # check Subtotal
        subtotal = 0.0
        restaurant_subtotal = restaurant_details["subtotal"]
        if restaurant_subtotal > 0:
            subtotal = item_total+vat+sc

        api_subtotal = data["bill"]["subtotal"]
        print(subtotal, "<- Subtotal ->", api_subtotal)
        assert subtotal == api_subtotal, "subtotal doesn't match!"
