import pprint
import sys

from food_order import FoodOrder
from search_restaurant import SearchResto
from search_item import ITEMCHOICE
from promo import PROMO
from calculation_assertion import CalculateBillAssertion


API_BASE = "https://api.example-stageenv.xyz"
FOOD_URL = "v1/me/foods"
FOOD_URL_NO_USER = "v1/foods"
FOOD_BASE_URL = f"{API_BASE}/{FOOD_URL}"
FOOD_BASE_URL_NO_USER = f"{API_BASE}/{FOOD_URL_NO_USER}"

USER_DETAILS = {
    "name": "Test User",
    "address": "Bokul, H 34, ABC, XYZ",
    "latitude": 00.0000,
    "longitude": 00.000,
    "city": "1",
    "country": "1"
}


class Authentication:
    HEADERS = {
        "App-Agent": "ride/android/433",
        "Android-OS": "11",
        "Authorization": "Bearer couAlQGtfWhfeKWxOuZEPzAMNjXenMkpobJtUmnj",
        "City-Id": USER_DETAILS["city"],
        "Country-Id": USER_DETAILS["country"]
    }


def run():
    search = SearchResto(
        api_base_url=FOOD_BASE_URL,
        api_base_url_no_user=FOOD_BASE_URL_NO_USER,
        headers=Authentication.HEADERS,
        user_details=USER_DETAILS
    )
    restaurant_details = search.run()
    if restaurant_details is not None:
        restaurant_id = restaurant_details["id"]
    else:
        print("no restaurant found. check console log for any error")
        sys.exit(0)

    item_rough = ITEMCHOICE(
        api_base_url=FOOD_BASE_URL,
        api_base_url_no_user=FOOD_BASE_URL_NO_USER,
        headers=Authentication.HEADERS,
        user_details=USER_DETAILS
    )
    cart_items, item_total = item_rough.run(restaurant_id=restaurant_id)  # take the id from the details
    promotion = PROMO(
        api_base_url=FOOD_BASE_URL,
        headers=Authentication.HEADERS,
        user_details=USER_DETAILS
    )
    promo_dict = promotion.run(restaurant_id)

    if len(cart_items) > 0:
        assertion = CalculateBillAssertion(
            api_base_url=FOOD_BASE_URL,
            headers=Authentication.HEADERS,
            user_details=USER_DETAILS
        )
        is_success = assertion.run_calculate_bill_flow(
            restaurant_details=restaurant_details,
            cart_items=cart_items,
            item_total=item_total,
            promo_code=promo_dict.get("promo_code", "")
        )

        if is_success:
            print("Assertion Passed. Now doing order flow....")
            order = FoodOrder(api_base_url=FOOD_BASE_URL, headers=Authentication.HEADERS)
            order.run_order_flow(
                restaurant_id=restaurant_id,
                user_details=USER_DETAILS,
                cart_items=cart_items,
                promo_code=promo_dict.get("promo_code", "")
            )
    else:
        print("cart is empty!")


if __name__ == "__main__":
    run()
