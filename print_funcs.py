# coding utf-8

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
