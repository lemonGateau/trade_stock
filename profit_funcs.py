from util import *

def compute_total_profit(sell_dic, buy_dic):
    ''' ToDo: length が異なる場合の計算 '''
    sell_list = list(sell_dic.values())
    buy_list = list(buy_dic.values()) 

    l = confirm_smaller_length(sell_dic, buy_dic)

    return int(sum(sell_list[-l:]) - sum(buy_list[-l:]))
