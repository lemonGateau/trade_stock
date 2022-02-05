from pandas_datareader import data
import pandas as pd
import datetime

from indicator_funcs import generate_sma, generate_ema, is_crossover
from strategy import Strategy

class Dmi(Strategy):
    def __init__(self, df_high, df_low, adx_term, adxr_term):
        self.high = df_high
        self.low  = df_low

        self.set_latest_buy_price(None)

        self.compute_tr()
        self.compute_dms()
        self.compute_dis(adx_term)
        self.compute_dx()
        self.compute_adx(adx_term)
        self.compute_adxr(adxr_term)

    def should_sell(self, i):
        if self.latest_buy_price is None:
            return False

        if self.adx[i] > 25 and is_crossover(self.minus_di[i-1:i+1], self.plus_di[i-1:i+1]):
            return True

        return False

    def should_buy(self, i):
        if self.latest_buy_price:
            return False

        if self.adx[i] > 25 and is_crossover(self.plus_di[i-1:i+1], self.minus_di[i-1:i+1]):
            return True

        return False

    def compute_tr(self):
        t1 = self.high        - self.low
        t2 = self.high        - self.low.shift()
        t3 = self.low.shift() - self.low

        self.tr = pd.concat([t1, t2, t3], axis=1).max(axis=1)

    def compute_dms(self):
        plus_dm  = self.high        - self.high.shift()
        minus_dm = self.low.shift() - self.low

        self.plus_dm, self.minus_dm = self.adjust_dms(plus_dm, minus_dm)

    def adjust_dms(self, plus_dm, minus_dm):
        for i in range(len(plus_dm)):
            plus_dm[i]  = max(plus_dm[i] , 0)
            minus_dm[i] = max(minus_dm[i], 0)

            # ※一致の場合、両方0
            if plus_dm[i] >= minus_dm[i]:
                minus_dm[i] = 0
            if plus_dm[i] <= minus_dm[i]:
                plus_dm[i]  = 0

        return plus_dm, minus_dm

    def compute_dis(self, term):
        sum_pdm = self.plus_dm.rolling(term).sum()
        sum_mdm = self.minus_dm.rolling(term).sum()
        sum_tr  = self.tr.rolling(term).sum()

        self.plus_di  = sum_pdm / sum_tr * 100
        self.minus_di = sum_mdm / sum_tr * 100

    def compute_dx(self):
        self.dx  = abs(self.plus_di - self.minus_di) / (self.plus_di + self.minus_di) * 100

    def compute_adx(self, term):
        self.adx = generate_ema(self.dx, term)

    def compute_adxr(self, term):
        self.adxr = generate_sma(self.adx, term)

    def get_dis(self):
        return self.plus_di, self.minus_di

    def get_adxs(self):
        return self.adx, self.adxr


if __name__ == '__main__':
    """
    START  = datetime.datetime(2021, 4, 1)
    END    = datetime.datetime.today()
    SYMBOL = "^N225"
    SOURCE = "yahoo"
    df = data.DataReader(SYMBOL, SOURCE, START, END)

    ADX_TERM  = 14
    ADXR_TERM = 20

    dmi = Dmi(df["High"], df["Low"], ADX_TERM, ADXR_TERM)
    
    print("tr", dmi.get_tr())
    print("dms", dmi.get_dms())
    print("dis", dmi.get_dis())
    print("dx", dmi.get_dx())
    print("adxs", dmi.get_adxs())
    """
