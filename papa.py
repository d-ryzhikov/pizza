#!/usr/bin/env python3
import json
from collections import namedtuple

import requests

Parentheses = namedtuple("Parentheses", "start end")


def parentheses_substr(s, pair: Parentheses):
    """
    >>> p = Parentheses("{", "}")
    >>> parentheses_substr("spam {top {kek}}", p)
    '{top {kek}}'
    """
    start_index = s.find(pair.start)
    if start_index == -1:
        raise ValueError("No start parenthesis found")
    substr = s[start_index:]
    depth = 0

    for index, char in enumerate(substr):
        if char == pair.end:
            depth -= 1
        if char == pair.start:
            depth += 1
        if char == pair.end and not depth:
            return substr[:index + 1]
    raise ValueError("No matching end parenthesis found")


MENU_URL = "https://www.papajohns.by/menyu/pizza"

GOODS_LOOKUP_STR = "glb.goods = {"


def papa_info():
    """Return info about Papa John's Menu"""
    resp = requests.get(MENU_URL)
    goods_start_index = resp.text.find(GOODS_LOOKUP_STR)
    goods_str = parentheses_substr(
        resp.text[goods_start_index + len(GOODS_LOOKUP_STR) - 1:],
        Parentheses(start="{", end="}")
    )
    return json.loads(goods_str)


if __name__ == "__main__":
    for item in papa_info()["pizzas"].values():
        if item.get("category_id") == "1":
            print(item.get("name"))
