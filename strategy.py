import pandas as pd
from common.plot_funcs import plot_df


class Strategy:
    def __init__(self):
        # self.set_latest_buy_price(None)
        # self.set_strategy_name()
        pass

    def should_buy(self, i):
        pass

    def should_sell(self, i):
        pass

    def set_latest_buy_price(self, buy_price):
        self.latest_buy_price = buy_price

    def get_latest_buy_price(self):
        return self.latest_buy_price

    def set_strategy_name(self, strat_name):
        self.strat_name = strat_name

    def get_strategy_name(self):
        return self.strat_name

    def build_df_indicator(self):
        indicator = pd.DataFrame()

    def plot_df_indicator(self):
        plot_df([self.build_df_indicator()])
