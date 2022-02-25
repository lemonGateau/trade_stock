import sys
sys.path.append("..")

from pandas_datareader import data
import pandas as pd
from common.print_funcs import *
from common.profit_funcs import *
from io_data import fetch_yahoo_short_bars

# ImportError: attempted relative import with no known parent package
try:
    from ..indicators import CombinationStrategy
except:
    from indicators import CombinationStrategy


def simulate_trade(strat, df_prices, show_detail=False, enable_plot=False):
    strat.set_latest_buy_price(None) # 初期化に必要
    sell_dic = {}
    buy_dic  = {}

    for i in range(1, len(df_prices)):
        latest_date  = df_prices.index[i]
        latest_price = df_prices[i]

        if strat.should_buy(i):
            # print_order(latest_date, latest_price, "buy")
            strat.set_latest_buy_price(latest_price)
            buy_dic[latest_date] = latest_price
    
        if strat.should_sell(i):
            # print_order(latest_date, latest_price, "sell")
            strat.set_latest_buy_price(None)
            sell_dic[latest_date] = latest_price

    print("{:20}".format(strat.get_strategy_name()), end=" ")

    if show_detail:
        total_profit = print_final_result(sell_dic, buy_dic)
    else:
        total_profit = print_summary_result(sell_dic, buy_dic)

    if enable_plot:
        strat.plot_df_indicator()

    return total_profit, len(sell_dic), len(buy_dic)


def simulate_grand_trade(strats, df_prices, required_buy_strats=[], required_sell_strats=[], show_detail=False, enable_plot=False):
    ''' stratsの全組み合わせでシミュレート '''
    buy_strats  = required_buy_strats
    sell_strats = required_sell_strats

    strat_names = []
    profits     = []
    sell_counts = []
    buy_counts  = []

    for buy_strat in strats:
        for sell_strat in strats:
            ustrat = CombinationStrategy(buy_strats + [buy_strat], sell_strats + [sell_strat])
            profit, sell_count, buy_count = simulate_trade(ustrat, df_prices, show_detail, enable_plot)

            strat_names.append(ustrat.get_strategy_name())
            profits.append(profit)
            sell_counts.append(sell_count)
            buy_counts.append(buy_count)

    columns = ('strategy', 'profit', 'sell_count', 'buy_count')

    return pd.DataFrame(data={'strategy': strat_names, 'profit': profits, \
        'sell_count': sell_counts, 'buy_count': buy_counts}, columns=columns)


def simulate_by_short_bars(strat, symbol, range, interval, show_detail=False, enable_plot=False):
    df = fetch_yahoo_short_bars(symbol, range, interval)

    return simulate_trade(strat, df["Adj Close"], show_detail, enable_plot)

def simulate_by_long_bars(strat, symbol, source, begin, end, show_detail=False, enable_plot=False):
    df = data.DataReader(symbol, source, begin, end)

    return simulate_trade(strat, df["Adj Close"], show_detail, enable_plot)
