import json
from datetime import datetime


def save_to_json(str1, str2, date_time):
    """
    Saves two strings and a datetime to a JSON file.

    :param str1: First string to save.
    :param str2: Second string to save.
    :param date_time: Datetime object to save.
    :param file_name: Name of the JSON file to save the data to.
    """
    file_name = "/home/akurtz/repeat-order-analysis/API/keys.json"
    # Convert datetime to a string in ISO format for JSON compatibility
    date_time_str = date_time.isoformat()

    # Create a dictionary with the data
    data = {"string1": str1, "string2": str2, "datetime": date_time_str}

    # Write the dictionary to a JSON file
    with open(file_name, "w") as file:
        json.dump(data, file, indent=4)


def save_output_to_json(file_path, data):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)


def read_from_json():
    """
    Reads two strings and a datetime from a JSON file.

    :param file_name: Name of the JSON file to read the data from.
    :return: Tuple containing two strings and a datetime object.
    """
    file_name = "/home/akurtz/repeat-order-analysis/API/keys.json"
    with open(file_name, "r") as file:
        data = json.load(file)

    # Extract the strings
    str1 = data["string1"]
    str2 = data["string2"]

    # Convert the datetime string back to a datetime object
    date_time = datetime.fromisoformat(data["datetime"])

    return str1, str2, date_time
