from profit_funcs import compute_total_profit

def print_df_date(df_index):
    print(f'{df_index.year:>4d}/{df_index.month:>2d}/{df_index.day:>2d}', end="  ")


def print_prices(price_list):
    for price in price_list:
        print(f'{int(price):>6d}', end=" ")

    print("\n", end="")

def print_order(df_index, order_price, side="sell"):
    print_df_date(df_index)
    print(side, end="\t")
    print_prices([order_price])


def print_all_trade_hist(trade_dic):
    for index, price in trade_dic.items():
        print_df_date(index)
        print_prices([price])
    print("\n", end="")


def print_summary_result(sell_dic, buy_dic):
    print(f'total_profit: {compute_total_profit(sell_dic, buy_dic):>6d}', end=" ")
    print(f'sell_count  : {len(sell_dic):>3d}', end=" ")
    print(f'buy_count   : {len(buy_dic) :>3d}', end="\n")


def print_final_result(sell_dic, buy_dic):
    """ 取引結果表示"""
    print("="*30)

    print("sell_history :")
    print_all_trade_hist(sell_dic)
    print("buy_history  :")
    print_all_trade_hist(buy_dic)

    print(f'sell_count  : {len(sell_dic)}')
    print(f'buy_count   : {len(buy_dic)}')
    print(f'total_profit: {compute_total_profit(sell_dic, buy_dic)}')

    print("="*30)
    print("\n")
