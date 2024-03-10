import etsy_api
from json_saving import save_to_json, read_from_json, save_output_to_json
from requests_oauthlib import OAuth2Session

access_token, refresh_token, date = read_from_json()


api = etsy_api.EtsyAPI(
    "xm01cxk1qnki67tzfe77r61m", access_token, refresh_token, date, save_to_json
)
api_data = api.get_shop_receipts(
    23574688, was_canceled=False, was_shipped=False, limit=100
)
save_output_to_json(
    "/home/akurtz/repeat-order-analysis/API/output.json", api_data
)
