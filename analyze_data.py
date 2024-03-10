"""
Analyze repeat customer order data from an Etsy shop
"""

from api_lib import get_all_orders

KEY_PATH = "/home/akurtz/repeat-order-analysis/API/keys.json"
DATA_PATH = "/home/akurtz/repeat-order-analysis/API/orders.json"
SHOP_ID = 23574688

get_all_orders(KEY_PATH, DATA_PATH, SHOP_ID)
