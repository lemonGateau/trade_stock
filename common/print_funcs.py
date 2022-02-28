
def print_df_date(df_index):
    print(f'{df_index.year:>4d}/{df_index.month:>2d}/{df_index.day:>2d}', end="  ")

def print_prices(price_list):
    for price in price_list:
        print(f'{int(price):>10d}', end="  ")

    print("\n", end="")

def print_reference_data_period(symbol, begin, end):
    print(symbol, end="  ")
    print_df_date(begin)
    print_df_date(end)
    print("\n")
