"""
Library to hand accessing Etsy API to pull order data and store keys
"""

import json
import requests

KEY_PATH = "keys.json"


def save_to_json(file_path, data):
    """
    Saves data to file_path as json

    Args:
        file_path: String representing filepath to save data to
        data: Dict to save as json

    """
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def read_json(file_path):
    """
    Reads json at file_path and returns corresponding dict

    Args:
        file_path: String representing filepath to get data from

    Returns dict with JSON data
    """
    with open(file_path, "r", encoding="utf-8") as file:
        data_dict = json.load(file)

    return data_dict


def save_key(file_path, new_key):
    """
    Updates the access and refresh token in file_path

    Args:
        file_path: String representing filepath to json with keys
        new_key: New token as dict with new access and refresh tokens
    """
    with open(file_path, "r", encoding="utf-8") as file:
        keys = json.load(file)

    keys["access_token"] = new_key["access_token"]
    keys["refresh_token"] = new_key["refresh_token"]

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(keys, file, indent=4)


def refresh_key(key_path):
    """
    Updates the key at path key_path with new access and refresh tokens

    Gets a new key from Etsy API using the key stored at the key_path JSON,
    then updates the key at key_path

    Args:
        key_path: String with path to json containing key
    """

    old_key = read_json(key_path)

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = {
        "grant_type": "refresh_token",
        "client_id": old_key["keystring"],
        "refresh_token": old_key["refresh_token"],
    }

    new_key = requests.post(
        "https://api.etsy.com/v3/public/oauth/token",
        headers=headers,
        data=data,
        timeout=100,
    )

    save_key(key_path, new_key.json())


def get_orders(key_path, shop_id, limit=100, offset=0):
    """
    Gets up to 100 order receipts from shop using Etsy API

    If the key at key_path has expired, it gets a new key.
    The function skips cancelled orders.

    Args:
        key_path: String with path to json containing key
        shop_id: String with shop id to get orders from
        limit: Int of range 0-100 representing how many orders to get
        offset: First how many orders to skip chronologically

    Returns a dict of orders with all data provided by API
    """
    key = read_json(key_path)

    headers = {
        "Authorization": f"Bearer {key['access_token']}",
        "x-api-key": key["keystring"],
    }

    orders_url = (
        f"https://openapi.etsy.com/v3/application/shops/{shop_id}"
        + f"/receipts?limit={limit}&offset={offset}&was_canceled=false"
    )
    orders = requests.get(orders_url, headers=headers, timeout=100)
    if orders.status_code != 200:
        refresh_key(key_path)
        key = read_json(key_path)
        headers["Authorization"] = f"Bearer {key['access_token']}"
        orders = requests.get(orders_url, headers=headers, timeout=100)

    return orders.json()


def get_reviews(key_path, shop_id, limit=100, offset=0):
    """
    Gets up to 100 reviews from shop using Etsy API

    If the key at key_path has expired, it gets a new key.

    Args:
        key_path: String with path to json containing key
        shop_id: String with shop id to get orders from
        limit: Int of range 0-100 representing how many orders to get
        offset: First how many orders to skip chronologically

    Returns a dict of reviews with all data provided by API
    """
    key = read_json(key_path)

    headers = {
        "Authorization": f"Bearer {key['access_token']}",
        "x-api-key": key["keystring"],
    }

    reviews_url = (
        f"https://openapi.etsy.com/v3/application/shops/{shop_id}"
        + f"/reviews?limit={limit}&offset={offset}"
    )
    reviews = requests.get(reviews_url, headers=headers, timeout=100)
    if reviews.status_code != 200:
        refresh_key(key_path)
        key = read_json(key_path)
        headers["Authorization"] = f"Bearer {key['access_token']}"
        reviews = requests.get(reviews_url, headers=headers, timeout=100)

    return reviews.json()


def get_all_orders(key_path, data_path, shop_id):
    """
    Gets all order receipts from an Etsy shop and saves them to a JSON

    Args:
        key_path: String with path to json containing api key
        data_path: String with path to where to save order data
        shop_id: Int representing Etsy shop id
    """

    first_order = get_orders(key_path, shop_id, limit=1)
    num_orders = int(first_order["count"])

    orders = []

    for index in range(0, num_orders + 1, 100):
        new_orders = get_orders(key_path, shop_id, offset=index)
        orders.extend(new_orders["results"])

    save_to_json(data_path, orders)


def get_all_reviews(key_path, data_path, shop_id):
    """
    Gets all order reviews from an Etsy shop and saves them to a JSON

    Args:
        key_path: String with path to json containing api key
        data_path: String with path to where to save order data
        shop_id: Int representing Etsy shop id
    """

    first_review = get_reviews(key_path, shop_id, limit=1)
    num_reviews = int(first_review["count"])

    reviews = []

    for index in range(0, num_reviews + 1, 100):
        new_reviews = get_reviews(key_path, shop_id, offset=index)
        reviews.extend(new_reviews["results"])

    save_to_json(data_path, reviews)
