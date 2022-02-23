from util import *


def compute_total_profit(sell_dic, buy_dic):
    ''' ToDo: length が異なる場合の計算 '''
    sell_list = list(sell_dic.values())
    buy_list = list(buy_dic.values()) 

    len = confirm_smaller_length(sell_dic, buy_dic)

    return int(sum(sell_list[:len]) - sum(buy_list[:len]))


def print_summary_result(sell_dic, buy_dic):
    total_profit = compute_total_profit(sell_dic, buy_dic)

    print(f'profit: {total_profit:>6d}'     , end=" ")
    print(f'sell_count: {len(sell_dic):>3d}', end=" ")
    print(f'buy_count : {len(buy_dic) :>3d}', end="\n")

    return total_profit


def print_final_result(sell_dic, buy_dic):
    """ 取引結果表示"""
    print("="*30)

    print("sell_history:")
    print_all_trade_hist(sell_dic)
    print("buy_history:")
    print_all_trade_hist(buy_dic)

    total_profit = print_summary_result(sell_dic, buy_dic)

    print("="*30)
    print("\n")

    return total_profit
