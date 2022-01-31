from util import *


def compute_total_profit(sell_dict, buy_dict):
    s = list(sell_dict.values())
    b = list(buy_dict.values()) 

    small_len = confirm_smaller_length(sell_dict, buy_dict)

    return sum(s[-small_len:]) - sum(b[-small_len:])
