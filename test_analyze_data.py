"""
Test functions in analyze_data file.
"""

from datetime import datetime
from analyze_data import (
    calculate_avg_order_size,
    calculate_orders_per_customer,
    calculate_reorder_rate_by_state,
    calculate_time_between_orders,
    count_orders_by_state,
    find_order_dates,
)


orders = [
    {
        "buyer_user_id": 1,
        "state": "VA",
        "subtotal": {"amount": 9000, "divisor": 100, "currency_code": "USD"},
        "create_timestamp": 1711485436,
    },
    {
        "buyer_user_id": 2,
        "state": "VA",
        "subtotal": {"amount": 4800, "divisor": 100, "currency_code": "USD"},
        "create_timestamp": 1711472846,
    },
    {
        "buyer_user_id": 3,
        "state": "TX",
        "subtotal": {"amount": 6000, "divisor": 100, "currency_code": "USD"},
        "create_timestamp": 1711413508,
    },
    {
        "buyer_user_id": 4,
        "state": "MA",
        "subtotal": {"amount": 3600, "divisor": 100, "currency_code": "USD"},
        "create_timestamp": 1711403198,
    },
    {
        "buyer_user_id": 4,
        "state": "VA",
        "subtotal": {"amount": 1200, "divisor": 100, "currency_code": "USD"},
        "create_timestamp": 1711400574,
    },
]


def test_calculate_orders_per_customer():
    """
    Test that all orders are counted correctly.
    """
    buyer_user_id, _, num_customers = calculate_orders_per_customer(orders)
    assert isinstance(buyer_user_id, list)
    assert len(buyer_user_id) == len(orders)
    assert sum(num_customers) == len(set(buyer_user_id))


def test_calculate_avg_order_size():
    """
    Test that all orders are classified correctly, and that the average
    order is more than 0$.
    """
    buyer_user_id, _, _ = calculate_orders_per_customer(orders)
    single_order_value, multiple_order_value = calculate_avg_order_size(
        buyer_user_id, orders
    )
    assert single_order_value > 0
    assert multiple_order_value > 0


def test_calculate_time_between_orders():
    """
    Test that all orders are classified correctly, and that the function
    returns the correct data types.
    """
    years, orders_by_customer = calculate_time_between_orders(
        [order["buyer_user_id"] for order in orders], orders
    )
    assert isinstance(years, list)
    assert isinstance(orders_by_customer, dict)


def test_find_order_dates():
    """
    Test that all orders are classified correctly to their group and month.
    """
    orders_by_customer = {1: [datetime(2021, 1, 1), datetime(2021, 2, 1)]}
    single_by_month, multiple_by_month = find_order_dates(orders_by_customer)
    assert single_by_month[0] == 0
    assert multiple_by_month[0] == 1
    assert multiple_by_month[1] == 1


def test_count_orders_by_state():
    """
    Test that all orders are classified correctly to their state.
    """
    state_list = count_orders_by_state(orders)
    assert not state_list.empty
    assert "MA" in state_list["state"].values


"""
def test_calculate_reorder_rate_by_state():
    state_reorder_df = calculate_reorder_rate_by_state(orders)
    assert not state_reorder_df.empty
"""
