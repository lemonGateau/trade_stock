import pandas as pd
from indicator_funcs import generate_ema
from strategy import Strategy
from print_funcs import *


class RsiCutler(Strategy):
    def __init__(self):
        pass

    def should_sell(self, i):
        pass

    def should_buy(self, i):
        pass

    def compute_rs(self, df_close, term):
        index = df_close.index
        rs   = [0]*term
        up   = [0]
        down = [0]

        for i in range(term+1, len(df_close)+1):
            for j in range(i-term, i):
                diff = df_close[j] - df_close[j-1]
                if diff > 0:
                    up.append(diff)
                    down.append(0)
                else:
                    up.append(0)
                    down.append(diff)

            sum_up = sum(up[i-term:i])
            sum_down = sum(down[i-term:i])

            rs.append(sum_up / (sum_up + abs(sum_down)) * 100)

            #print_df_date(index[j])
            #print_prices([df_close[j], df_close[j] - df_close[j-1], up[j], down[j], rs[j]])

        self.rs = pd.DataFrame(data=rs, index=index)

        print("d\t\tclose\tdiff\tup\tdown\trs")
        j = 0
        print_df_date(index[j])
        print_prices([df_close[j], 0, up[j], down[j], rs[j]])
        
        for j in range(1, len(df_close)):
            print_df_date(index[j])
            print_prices([df_close[j], df_close[j] - df_close[j-1], up[j], down[j], rs[j]])

    def get_rsi(self):
        return self.rs
