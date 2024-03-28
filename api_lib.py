"""
Library to handle accessing Etsy API to pull order data and store keys
"""

import json
import requests


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

    Returns:
        Dict with JSON data
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

    Returns:
        Dict of orders with all data provided by API
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

    cleaned_orders = clean_anonymize(orders)

    save_to_json(data_path, cleaned_orders)


def clean_anonymize(order_data):
    """
    Filters data so only relavant data is left show and anonymizes IDs

    It only leaves the state, subtotal, create_timestamp, and numbers
    in place of buyer_user_id so that it isn't a real id.

    Args:
        order_data: List of dicts of Etsy order data from reciepts endpoint

    Returns:
        List of dicts with only relavant data and anonymized ids
    """

    cleaned_data = []

    new_id = 1
    id_dict = {}

    for order in order_data:
        order_dict = {}
        if order["buyer_user_id"] not in id_dict:
            id_dict[order["buyer_user_id"]] = new_id
            order_dict["buyer_user_id"] = new_id
            new_id += 1
        else:
            order_dict["buyer_user_id"] = id_dict[order["buyer_user_id"]]
        order_dict["state"] = order["state"]
        order_dict["subtotal"] = order["subtotal"]
        order_dict["create_timestamp"] = order["create_timestamp"]
        cleaned_data.append(order_dict)

    return cleaned_data


def extract_data(data, parameter_1, parameter_2=None):
    """
    Extracts the data stored in the parameter from each order.

    This function assumes parameter_1 and parameter_2 if specified exist in all
    dicts in the list.

    Args:
        data: List of dicts that have keys parameter_1 and parameter_2 if
        specified
        parameter_1: Key to pull data from. It should be same datatype as key
        in dict
        parameter_1: Key to pull data from. It should be same datatype as key
        in dict

    Returns:
        If both parameter_1 and parameter_2 are given, returns a 2d list with
        the first column being parameter_1's values and the second
        parameter_2's with each row being the data from the same order.
    """
    extracted_data = []

    if parameter_2 is not None:
        for i, _ in enumerate(data):
            data_pair = []
            data_pair.append(data[i][parameter_1])
            data_pair.append(data[i][parameter_2])
            extracted_data.append(data_pair)
    else:
        for i, _ in enumerate(data):
            extracted_data.append(data[i][parameter_1])

    return extracted_data
