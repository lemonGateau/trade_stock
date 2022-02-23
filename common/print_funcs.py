
def print_df_date(df_index):
    print(f'{df_index.year:>4d}/{df_index.month:>2d}/{df_index.day:>2d}', end="  ")

def print_simulation_conditions(symbol, start, end):
    print(symbol, end="  ")
    print_df_date(start)
    print_df_date(end)
    print("\n")

def print_prices(price_list):
    for price in price_list:
        print(f'{int(price):>10d}', end=" ")

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
    print("\n")


def print_extract_strats_df(df, buy_strat="", sell_strat=""):
    ''' 特定の戦略を含む取引結果を表示する ''' 
    # -- より前(買い戦略)と -- より後(売り戦略)に分割
    buy_strats  = df['strategy'].str.split(pat='--', expand=True)[0]
    sell_strats = df['strategy'].str.split(pat='--', expand=True)[1]

    if buy_strat:
        df = df.loc[buy_strats.str.contains(buy_strat)]
    if sell_strat:
        df = df.loc[sell_strats.str.contains(sell_strat)]

    print("{:6}--{:6}".format(buy_strat, sell_strat))
    print_sorted_df(df, 'profit', False)
