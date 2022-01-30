# coding utf-8
import pandas
from trade1 import *

class SmaCross:
    def __init__(self, short_sma, long_sma):
        self.short_sma = short_sma
        self.long_sma  = long_sma

    def execute(self, i):
        if is_crossover(self.short_sma[i-1:i+1], self.long_sma[i-1:i+1]):
            buy()
            print("buy")

        elif is_crossover(self.long_sma[i-1:i+1], self.short_sma[i-1:i+1]):
            sell()
            print("sell")

