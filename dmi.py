from pandas_datareader import data
import pandas as pd
import datetime
from indicator_funcs import generate_sma, generate_ema, is_crossover
from strategy import Strategy

class Dmi(Strategy):
    def __init__(self, df_high, df_low, adx_term, adxr_term):
        self.df = pd.DataFrame()
        self.df["High"] = df_high
        self.df["Low"]  = df_low

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

        if self.df["adx"][i] > 25 and is_crossover(self.df["m_di"][i-1:i+1], self.df["p_di"][i-1:i+1]):
            return True

        return False

    def should_buy(self, i):
        if self.latest_buy_price:
            return False

        if self.df["adx"][i] > 25 and is_crossover(self.df["p_di"][i-1:i+1], self.df["m_di"][i-1:i+1]):
            return True

        return False

    def compute_tr(self):
        t1 = self.df["High"]        - self.df["Low"]
        t2 = self.df["High"]        - self.df["Low"].shift()
        t3 = self.df["Low"].shift() - self.df["Low"]

        self.df["tr"] = pd.concat([t1, t2, t3], axis=1).max(axis=1)

    def compute_dms(self):
        df = pd.DataFrame()

        df["p_dm"] = self.df["High"]        - self.df["High"].shift()
        df["m_dm"] = self.df["Low"].shift() - self.df["Low"]

        self.df["p_dm"], self.df["m_dm"] = self.adjust_dms(df)

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
        sum_pdm = self.df["p_dm"].rolling(term).sum()
        sum_mdm = self.df["m_dm"].rolling(term).sum()
        sum_tr  = self.df["tr"].rolling(term).sum()

        self.df["p_di"] = sum_pdm / sum_tr * 100
        self.df["m_di"] = sum_mdm / sum_tr * 100

    def compute_dx(self):
        self.df["dx"] = abs(self.df["p_di"] - self.df["m_di"]) / (self.df["p_di"] + self.df["m_di"]) * 100

    def compute_adx(self, term):
        self.df["adx"] = generate_ema(self.df["dx"], term)

    def compute_adxr(self, term):
        self.df["adxr"] = generate_sma(self.df["adx"], term)

    def get_dis(self):
        return self.df["p_di"], self.df["m_di"]

    def get_adxs(self):
        return self.df["adx"], self.df["adxr"]
