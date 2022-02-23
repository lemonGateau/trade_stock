import pandas as pd
from common.print_funcs import *
from common.profit_funcs import *
from combinationStrategy import CombinationStrategy


def simulate_trade(strat, df_prices):
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
    total_profit = print_summary_result(sell_dic, buy_dic)
    # total_profit = print_final_result(sell_dic, buy_dic)

    strat.plot_df_indicator()

    return total_profit, len(sell_dic), len(buy_dic)


def simulate_grand_trade(strats, df_prices, required_buy_strats=[], required_sell_strats=[]):
    ''' stratsの全組み合わせでシミュレート '''
    buy_strats  = required_buy_strats
    sell_strats = required_sell_strats

    strat_names = []
    profits     = []
    sell_counts = []
    buy_counts  = []

    for buy_strat in strats:
        for sell_strat in strats:
            ustrat = UniqueStrategy1(buy_strats + [buy_strat], sell_strats + [sell_strat])
            profit, sell_count, buy_count = simulate_trade(ustrat, df_prices)

            strat_names.append(ustrat.get_strategy_name())
            profits.append(profit)
            sell_counts.append(sell_count)
            buy_counts.append(buy_count)
    print("\n")

    columns = ('strategy', 'profit', 'sell_count', 'buy_count')

    return pd.DataFrame(data={'strategy': strat_names, 'profit': profits, \
        'sell_count': sell_counts, 'buy_count': buy_counts}, columns=columns)



