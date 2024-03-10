import requests_oauthlib as OAuth2Session
import requests
from json_saving import save_to_json, read_from_json, save_output_to_json

KEYSTRING = "xm01cxk1qnki67tzfe77r61m"

token = {
    "access_token": "314203756.txwWFjORiD8KwIYQdpdqVC61u9uL46dz-8p2sE9E7RWOF5OmhUJdB2M-i40n2pwuopZot65X6ALmQkG3tGcAVNmOaK",
    "token_type": "Bearer",
    "expires_in": 3600,
    "refresh_token": "314203756.KQbgemldIvQuJQrvNOVylHEBwOr6w_pp_SPL5XVEFAcKaMCFCDpLl1ITFo0f8nqFJgMdmkAk58xdvKt5U0RF3yGFt2",
}

REFRESH_URL = "https://api.etsy.com/v3/public/oauth/token"

etsy_auth = OAuth2Session(
    KEYSTRING,
    token=token,
    auto_refresh_url=REFRESH_URL,
)

headers = {
    "Accept": "application/json",
    "Content-Type": "application/x-www-form-urlencoded",
    "x-api-key": KEYSTRING,
}

SHOP_ID = 23574688

first_order = etsy_auth.get(
    f"https://openapi.etsy.com/v3/application/shops/{SHOP_ID}/receipts",
    headers=headers,
)

first_order_dict = first_order.json()

num_orders = int(first_order_dict["count"])

orders = []

for index in range(0, num_orders + 1, 100):
    new_orders = etsy_auth.get(
        f"https://openapi.etsy.com/v3/application/shops/{SHOP_ID}/receipts?limit=100&offset={index}&was_canceled=false",
        headers=headers,
    ).json()

    orders.extend(new_orders["results"])

save_output_to_json(
    "/home/akurtz/repeat-order-analysis/API/output.json", orders
)

print(len(orders))
