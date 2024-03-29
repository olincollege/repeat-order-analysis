"""
Analyze repeat customer order data from an Etsy shop
"""

from collections import Counter
from datetime import datetime
import statistics
import pandas as pd
from api_lib import extract_data

KEY_PATH = "keys.json"
ORDERS_PATH = "orders.json"
SHOP_ID = 23574688


def calculate_orders_per_customer(orders):
    """
    Calculates the distribution of orders per customer, excluding a specific
    outlier.

    Args:
        orders (list): A list of all order data

    Returns:
        num_reorders (list): The number of orders placed by customers
        num_customers (list): The number of customers placing a certain number
        of orders
    """
    buyer_user_id = extract_data(orders, "buyer_user_id")

    num_orders_by_customers = list(Counter(buyer_user_id).values())

    if 37 in num_orders_by_customers:
        num_orders_by_customers.remove(37)

    orders_per_customer = Counter(num_orders_by_customers)

    num_reorders = orders_per_customer.keys()
    num_customers = orders_per_customer.values()

    return buyer_user_id, num_reorders, num_customers


def calculate_avg_order_size(buyer_user_id, orders):
    """
    Calculate the average order value for single-order and multiple-order
    customers.

    Args:
        buyer_user_id (list): A list of all ids of customers that placed orders
        orders (list): A list of all order data

    Returns:
        single_order_value (float): The average value of non-repeat orders
        multiple_order_value (float): The average value of repeat orders
    """
    id_subtotal_dict = extract_data(orders, "buyer_user_id", "subtotal")
    num_orders_by_id = Counter(buyer_user_id)

    id_subtotal = []
    for customer in id_subtotal_dict:
        id_subtotal.append(
            [customer[0], customer[1]["amount"] / customer[1]["divisor"]]
        )

    single_order_customers = []
    multiple_order_customers = []

    for customer in id_subtotal:
        if num_orders_by_id[customer[0]] > 1:
            multiple_order_customers.append(customer[1])
        else:
            single_order_customers.append(customer[1])

    single_order_value = statistics.mean(single_order_customers)
    multiple_order_value = statistics.mean(multiple_order_customers)

    return single_order_value, multiple_order_value


def calculate_time_between_orders(buyer_user_id, orders):
    """
    Calculate the time delta in years between orders for repeat customers.

    Args:
        buyer_user_id (list): A list of all ids of customers that placed orders
        orders (list): A list of all order data

    Returns:
        years (list): A list of time deltas between orders
    """
    order_time = extract_data(orders, "create_timestamp")

    for i, timestamp in enumerate(order_time):
        order_time[i] = datetime.fromtimestamp(timestamp)

    orders_by_customer = {}

    for customer_id, order_time in zip(buyer_user_id, order_time):
        if customer_id not in orders_by_customer:
            orders_by_customer[customer_id] = []
        orders_by_customer[customer_id].append(order_time)

    all_time_diffs = []

    for times in orders_by_customer.values():
        times.sort()
        if len(times) > 1:
            all_time_diffs.extend(
                [times[i] - times[i - 1] for i in range(1, len(times))]
            )

    years = [t.days / 365.25 for t in all_time_diffs]

    return years, orders_by_customer


def find_order_dates(orders_by_customer):
    """
    Counts the number of orders that occur in any given month.

    Args:
        orders_by_customer (dict): A dictionary linking customer ids to their
        order times

    Returns:
        single_by_month (list): A tally of the number of orders happening in a
        given month for non-repeat customers.
        multiple_by_month (list): A tally of the number of orders happening in
        a given month for repeat customers.

    """
    mult_cust_times = {}
    single_cust_times = {}

    for ids, dates in orders_by_customer.items():
        if len(dates) > 1:
            mult_cust_times[ids] = dates
        else:
            single_cust_times[ids] = dates

    single_by_month = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    multiple_by_month = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    for ids, dates in mult_cust_times.items():
        for date_time in dates:
            month = date_time.month
            multiple_by_month[month - 1] += 1

    for ids, dates in single_cust_times.items():
        single_by_month[dates[0].month - 1] += 1

    return single_by_month, multiple_by_month


def count_orders_by_state(orders):
    """
    Counts the number of orders shipped to each US state

    Args:
        orders (list): A list of all order data

    Returns:
        state_list (dict): A dictionary mapping the number of orders occurring
        in a state to the state name

    """
    state = extract_data(orders, "state")

    state_list = Counter(state)
    state_list = pd.DataFrame.from_dict(
        state_list, orient="index"
    ).reset_index()
    state_list = state_list.rename(
        columns={"index": "state", 0: "number_of_orders"}
    )

    return state_list


def calculate_reorder_rate_by_state(orders):
    """
    Calculates the percentage of customer that place more than one order by
    US state.

    Args:
        orders (list): A list of all order data

    Returns:
        state_reorder_df (df): A DataFrame mapping the reorder percentages to
        the state name

    """
    id_state = extract_data(orders, "buyer_user_id", "state")
    state = extract_data(orders, "state")

    all_states_list = list(Counter(state).keys())
    states_dict = {key: [] for key in all_states_list}

    for customer in id_state:
        states_dict[customer[1]].append(customer[0])

    percent_reorder_by_state = {}
    for state, _ in states_dict.items():
        num_orders = Counter(Counter(states_dict[state]).values())
        one_order = 0
        multiple_orders = 0
        for number_of_orders, number_of_customers in num_orders.items():
            if number_of_orders == 1:
                one_order += number_of_customers
            if number_of_orders > 1:
                multiple_orders += number_of_customers
        if one_order + multiple_orders > 20:
            percent_reorder_by_state[state] = multiple_orders / (
                one_order + multiple_orders
            )

    state_reorder_df = pd.DataFrame.from_dict(
        percent_reorder_by_state, orient="index"
    ).reset_index()
    state_reorder_df = state_reorder_df.rename(
        columns={"index": "state", 0: "reorder_rate"}
    )

    state_reorder_df["reorder_rate"] = state_reorder_df["reorder_rate"] * 100

    return state_reorder_df
