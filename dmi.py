import pandas as pd

class Dmi:
    def __init__(self, df_high, df_low):
        self.high = df_high
        self.low  = df_low

    def should_sell(self, i):
        pass

    def should_buy(self, i):
        pass

    def compute_tr(self):
        """ 
        tr(true range): max((当日の高値-当日の安値),
                            (当日の高値-前日の終値),
                            (前日の終値-当日の安値))
        """
        t1 = self.high        - self.low
        t2 = self.high        - self.low.shift()
        t3 = self.low.shift() - self.low

        tr = []

        for i in range(len(self.high)):
            tr.append(max(t1[i], t2[i], t3[i]))

        self.tr = pd.DataFrame(data=tr, index=self.high.index)
    
    def get_tr(self):
        return self.tr

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

    def get_dms(self):
        return self.plus_dm, self.minus_dm

    def compute_dis(self, term):
        a = self.plus_dm.rolling(term).sum()
        b = self.tr.rolling(term).sum()

        plus_di = pd.DataFrame(data=a/b*100, index=a.index)

        print(plus_di)
