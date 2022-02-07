import pandas as pd
from indicator_funcs import *
from plot_funcs import plot_df
from print_funcs import *
from strategy import Strategy

class BolligerBands(Strategy):
    def __init__(self, df_close, term):
        self.df = pd.DataFrame()

        self.close = df_close
        self.std   = df_close.rolling(term).std()
        self.sma   = generate_sma(df_close, term)

        self.set_upper(coef=3)
        self.set_lower(coef=3)

        self.set_latest_buy_price(None)
        self.set_strategy_name("bbands")

        # print(self.df)

    def should_sell(self, i):
        if self.latest_buy_price is None:
            return False

        return self.close[i] > self.upper[i]

    def should_buy(self, i):
        if self.latest_buy_price:
            return False

        return self.close[i] < self.lower[i]

    def set_upper(self, coef=3):
        self.upper = self.sma + coef * self.std

    def set_lower(self, coef=3):
        self.lower = self.sma - coef * self.std

    def get_upper(self):
        return self.upper

    def get_lower(self):
        return self.lower

    def build_df_indicator(self):
        indicator = pd.DataFrame()

        indicator["Close"] = self.close
        indicator["middle"] = self.sma
        indicator["upper"] = self.upper
        indicator["lower"] = self.lower

        return indicator

    def plot_df_indicator(self):
        plot_df([self.build_df_indicator()])
