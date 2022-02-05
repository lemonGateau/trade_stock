import pandas
from indicator_funcs import *
from print_funcs import *
from strategy import Strategy

class Cross(Strategy):
    def __init__(self, ma1, ma2):
        self.ma1 = ma1
        self.ma2 = ma2
        self.set_latest_buy_price(None)

    def should_sell(self, i):
        if self.latest_buy_price is None:
            return False

        return is_crossover(self.ma1[i-1:i+1], self.ma2[i-1:i+1])

    def should_buy(self, i):
        if self.latest_buy_price:
            return False

        return is_crossover(self.ma2[i-1:i+1], self.ma1[i-1:i+1])
