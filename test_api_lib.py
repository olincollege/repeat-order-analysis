"""
Test functions in api_lib library.
"""

import pytest
from api_lib import extract_data, clean_anonymize, get_orders, read_json

KEY_PATH = "keys.json"
ORDERS_PATH = "orders.json"
SHOP_ID = 23574688

extract_data_cases = [
    # Test that it works with only parameter_1
    (
        [{"name": "Andrew", "age": 19}, {"name": "Joe", "age": 55}],
        "name",
        None,
        ["Andrew", "Joe"],
    ),
    # Test that it works with both parameter_1 and parameter_2
    (
        [{"name": "Andrew", "age": 19}, {"name": "Joe", "age": 55}],
        "name",
        "age",
        [["Andrew", 19], ["Joe", 55]],
    ),
    # Test it works with reversed order
    (
        [{"name": "Andrew", "age": 19}, {"name": "Joe", "age": 55}],
        "age",
        "name",
        [[19, "Andrew"], [55, "Joe"]],
    ),
    # Test different key types
    (
        [{"name": "Andrew", 1: "one"}, {"name": "Joe", 1: "one"}],
        1,
        None,
        ["one", "one"],
    ),
    # Test it works with nested dicts
    # Test that it works with both parameter_1 and parameter_2
    (
        [
            {"name": {"first": "Andrew", "last": "Kurtz"}, "age": 19},
            {"name": {"first": "Joe", "last": "Mama"}, "age": 55},
        ],
        "name",
        None,
        [
            {"first": "Andrew", "last": "Kurtz"},
            {"first": "Joe", "last": "Mama"},
        ],
    ),
]

clean_anonymize_cases = [
    # Test that it works with different buyer_user_ids
    (
        [
            {
                "buyer_user_id": 4023984,
                "ship name": "Andrew Kurtz",
                "address": "123 Main St",
                "state": "MA",
                "subtotal": {
                    "amount": 4000,
                    "divisor": 100,
                    "currency_code": "USD",
                },
                "create_timestamp": 123456789,
            },
            {
                "buyer_user_id": 8542943928,
                "ship name": "Iluv Sofdez",
                "address": "1000 Going Insane Way",
                "state": "MA",
                "subtotal": {
                    "amount": 3000,
                    "divisor": 100,
                    "currency_code": "USD",
                },
                "create_timestamp": 98372489,
            },
        ],
        [
            {
                "buyer_user_id": 1,
                "state": "MA",
                "subtotal": {
                    "amount": 4000,
                    "divisor": 100,
                    "currency_code": "USD",
                },
                "create_timestamp": 123456789,
            },
            {
                "buyer_user_id": 2,
                "state": "MA",
                "subtotal": {
                    "amount": 3000,
                    "divisor": 100,
                    "currency_code": "USD",
                },
                "create_timestamp": 98372489,
            },
        ],
    ),
    # Test that it works with same buyer_user_ids
    (
        [
            {
                "buyer_user_id": 4023984,
                "ship name": "Andrew Kurtz",
                "address": "123 Main St",
                "state": "MA",
                "subtotal": {
                    "amount": 4000,
                    "divisor": 100,
                    "currency_code": "USD",
                },
                "create_timestamp": 123456789,
            },
            {
                "buyer_user_id": 4023984,
                "ship name": "Iluv Sofdez",
                "address": "1000 Going Insane Way",
                "state": "MA",
                "subtotal": {
                    "amount": 3000,
                    "divisor": 100,
                    "currency_code": "USD",
                },
                "create_timestamp": 98372489,
            },
        ],
        [
            {
                "buyer_user_id": 1,
                "state": "MA",
                "subtotal": {
                    "amount": 4000,
                    "divisor": 100,
                    "currency_code": "USD",
                },
                "create_timestamp": 123456789,
            },
            {
                "buyer_user_id": 1,
                "state": "MA",
                "subtotal": {
                    "amount": 3000,
                    "divisor": 100,
                    "currency_code": "USD",
                },
                "create_timestamp": 98372489,
            },
        ],
    ),
]


def test_read_json():
    """
    Test that read_json successfully reads the order data at ORDER_PATH
    """
    output = read_json(ORDERS_PATH)
    assert isinstance(output, list)
    assert isinstance(output[0], dict)
    for order in output:
        assert "buyer_user_id" in order
        assert "state" in order


def test_get_orders():
    """
    Test that get_orders calls API correctly and returns data in correct format
    """
    output = get_orders(KEY_PATH, SHOP_ID)
    assert isinstance(output, dict)
    assert "results" in output
    for index, _ in enumerate(output):
        assert "buyer_user_id" in output["results"][index]
        assert "state" in output["results"][index]


@pytest.mark.parametrize(
    "data,parameter_1,parameter_2,result", extract_data_cases
)
def test_extract_data(data, parameter_1, parameter_2, result):
    """
    Test that extra_data extracts the correct data from the dict

    Args:
        data: List of dicts that have keys parameter_1 and parameter_2 if
        specified
        parameter_1: Key to pull data from. It should be same datatype as key
        in dict
        parameter_1: Key to pull data from. It should be same datatype as key
        in dict
        result: list that extract_data should return with extracted data
    """

    output = extract_data(data, parameter_1, parameter_2=parameter_2)
    assert isinstance(output, list)
    assert output == result


@pytest.mark.parametrize("order_data,result", clean_anonymize_cases)
def test_clean_anonymize(order_data, result):
    """
    Test that clean_anonymize correctly cleans and anonymizes the data

    Args:
        order_data: List of dicts of Etsy order data from reciepts endpoint
        result: List of dicts of correctly cleaned data
    """
    output = clean_anonymize(order_data)
    assert isinstance(output, list)
    assert output == result
