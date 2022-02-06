import pandas as pd
from indicator_funcs import is_crossover
from indicator_funcs import generate_sma
from strategy import Strategy

class Momentum(Strategy):
    def __init__(self):
        self.set_baseline_value(0)

        self.set_latest_buy_price(None)
        self.set_strategy_name("mom")

    def should_sell(self, i):
        if self.latest_buy_price is None:
            return False

        if is_crossover([self.base]*2, self.moment[i-1:i+1]):
            return True

        if self.moment[i] >= self.base and is_crossover(self.signal[i-1:i+1], self.moment[i-1:i+1]):
            return True

        return False

    def should_buy(self, i):
        if self.latest_buy_price:
            return False

        # ゼロラインを超えた時
        if is_crossover(self.moment[i-1:i+1], [self.base]*2):
            return True

        if self.moment[i] <= self.base and is_crossover(self.moment[i-1:i+1], self.signal[i-1:i+1]):
            return True

        return False

    def compute_moment(self, df_close, term):
        self.moment = df_close - df_close.shift(term)

    def get_moment(self):
        return self.moment

    def generate_signal(self, term):
        self.signal = generate_sma(self.moment, term)

    def get_signal(self):
        return self.signal

    def set_baseline_value(self, baseline_value):
        self.base = baseline_value

    def get_baseline_value(self):
        return self.base
