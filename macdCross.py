# coding utf-8
import pandas
from trade1 import *

class MacdCross:
    def __init__(self, macd, signal):
        self.macd   = macd
        self.signal = signal

    def execute(self, i):
        if is_crossover(self.macd[i-1:i+1], self.signal[i-1:i+1]):
            buy()
            print("buy")

        elif is_crossover(self.signal[i-1:i+1], self.macd[i-1:i+1]):
            sell()
            print("sell")