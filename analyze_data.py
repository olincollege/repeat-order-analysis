"""
Analyze repeat customer order data from an Etsy shop
"""

from api_lib import get_all_orders

KEY_PATH = "keys.json"
ORDERS_PATH = "orders.json"
REVIEWS_PATH = "reviews.json"
SHOP_ID = 23574688

get_all_orders(KEY_PATH, ORDERS_PATH, SHOP_ID)
