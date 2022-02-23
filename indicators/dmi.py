from pandas_datareader import data
import pandas as pd
import datetime

from common.indicator_funcs import *
from common.plot_funcs import plot_df
from common.print_funcs import *
from strategy import Strategy

class Dmi(Strategy):
    def __init__(self, df_close, df_high, df_low, adx_term, adxr_term):
        self.close = df_close
        self.high  = df_high
        self.low   = df_low

        self.compute_tr()
        self.compute_dms()
        self.compute_dis(adx_term)
        self.compute_dx()
        self.compute_adx(adx_term)
        self.compute_adxr(adxr_term)

        self.set_latest_buy_price(None)
        self.set_strategy_name("dmi")

        # print(self.df)

    def should_sell(self, i):
        if self.latest_buy_price is None:
            return False

        if self.adx[i] > 25 and is_crossover(self.m_di[i-1:i+1], self.p_di[i-1:i+1]):
            return True

        return False

    def should_buy(self, i):
        if self.latest_buy_price:
            return False

        if self.adx[i] > 25 and is_crossover(self.p_di[i-1:i+1], self.m_di[i-1:i+1]):
            return True

        return False

    def compute_tr(self):
        t1 = self.high          - self.low
        t2 = self.high          - self.close.shift()
        t3 = self.close.shift() - self.low

        self.tr = pd.concat([t1, t2, t3], axis=1).max(axis=1)

    def compute_dms(self):
        df = pd.DataFrame()

        df["p_dm"] = self.high        - self.high.shift()
        df["m_dm"] = self.low.shift() - self.low

        self.p_dm, self.m_dm = self.adjust_dms(df)

    def adjust_dms(self, df):
        # 一致なら両方0
        df.loc[df["p_dm"] == df["m_dm"], ["p_dm", "m_dm"]] = 0

        # 0未満なら0
        df.loc[df["p_dm"] < 0, "p_dm"] = 0
        df.loc[df["m_dm"] < 0, "m_dm"] = 0

        # 小さい方は0
        df.loc[df["p_dm"] < df["m_dm"] , "p_dm"] = 0
        df.loc[df["m_dm"] < df["p_dm"] , "m_dm"] = 0

        return df["p_dm"], df["m_dm"]

    def compute_dis(self, term):
        sum_pdm = self.p_dm.rolling(term).sum()
        sum_mdm = self.m_dm.rolling(term).sum()
        sum_tr  = self.tr.rolling(term).sum()

        self.p_di = sum_pdm / sum_tr * 100
        self.m_di = sum_mdm / sum_tr * 100

    def compute_dx(self):
        self.dx = abs(self.p_di - self.m_di) / (self.p_di + self.m_di) * 100

    def compute_adx(self, term):
        self.adx = generate_ema(self.dx, term)

    def compute_adxr(self, term):
        self.adxr = generate_sma(self.adx, term)

    def build_df_indicator(self):
        indicator = pd.DataFrame()

        indicator["plus_di"]     = self.p_di
        indicator["minus_di"]    = self.m_di
        indicator["adx"]         = self.adx

        return indicator

    def plot_df_indicator(self):
        plot_df([self.build_df_indicator()])
