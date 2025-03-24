"""Help functions"""

import logging


def call(
    func,
    count,
) -> list:
    """Call function any count of times with init null array of func result"""
    arr = []
    while count >= 1:
        arr.append(func())
        count -= 1
    return arr


def convert_args(rest):
    """Convert to key words arguments"""
    simple_args = {}
    for el in rest:
        if "=" in el:
            key, value = el.split("=")
            simple_args[key] = value.split(",") if "," in value else value
    return simple_args


def capitalize(word):
    """Capitalize word"""
    return word.capitalize()


def log_query_result(result):
    """Logging success or not result"""
    if result:
        logging.info("Query successded return result %s", result)
    else:
        logging.error("Query has not return result %s", result)
