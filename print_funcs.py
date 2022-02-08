
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


def print_sorted_df(df, by="profit", ascending=True):
    print(df.sort_values(by=by, ascending=ascending))
