import pandas as pd

from common.indicator_funcs import *
from common.plot_funcs import plot_df
from common.print_funcs import *
from strategy import Strategy

class Momentum(Strategy):
    def __init__(self):
        self.set_latest_buy_price(None)
        self.set_strategy_name("mom")

    def should_sell(self, i):
        if self.latest_buy_price is None:
            return False

        if is_crossover(self.baseline[i-1:i+1], self.moment[i-1:i+1]):
            return True

        if self.moment[i] >= self.baseline[i] and is_crossover(self.signal[i-1:i+1], self.moment[i-1:i+1]):
            return True

        return False

    def should_buy(self, i):
        if self.latest_buy_price:
            return False

        # ゼロラインを超えた時
        if is_crossover(self.moment[i-1:i+1], self.baseline[i-1:i+1]):
            return True

        if self.moment[i] <= self.baseline[i] and is_crossover(self.moment[i-1:i+1], self.signal[i-1:i+1]):
            return True

        return False

    def compute_moment(self, df_close, term):
        self.moment = df_close - df_close.shift(term)

    def generate_signal(self, term):
        self.signal = generate_sma(self.moment, term)

    def generate_baseline(self, base_value):
        self.baseline =  pd.DataFrame(data=[base_value]*len(self.moment), index=self.moment.index, columns=["base"])["base"]

    def build_df_indicator(self):
        indicator = pd.DataFrame()

        indicator["moment"]     = self.moment
        indicator["mom_signal"] = self.signal
        indicator["mom_base"]   = self.baseline

        return indicator

    def plot_df_indicator(self):
        plot_df([self.build_df_indicator()])
