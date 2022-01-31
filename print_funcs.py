from profit_funcs import compute_total_profit

def print_df_date(index):
    print(f'{index.year:>4d}/{index.month:>2d}/{index.day:>2d}', end="  ")


def print_prices(price_list):
    for price in price_list:
        print(f'{int(price):>6d}', end=" ")

    print("\n", end="")


def print_trade_hist(trade_dict):
    for index, price in trade_dict.items():
        print_df_date(index)
        print_prices([price])
    print("\n", end="")


def print_trade_result(sell_dict, buy_dict):
    """ 取引結果表示"""
    print(f'sell_count: {len(sell_dict)} buy_count: {len(buy_dict)}')
    print(f'total_profit: {compute_total_profit(sell_dict, buy_dict):>10d}\n')

    print("sell_history: ")
    print_trade_hist(sell_dict)
    print("buy_history:")
    print_trade_hist(buy_dict)

