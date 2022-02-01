from indicator_funcs import should_realize_profit, should_stop_loss


class FinalizedProfit():
    def __init__(self, profit_ratio, loss_ratio, df_close, add_strategy):
        self.profit_ratio = profit_ratio
        self.loss_ratio   = loss_ratio
        self.df_close = df_close
        self.add_strategy = add_strategy
        self.set_latest_buy_price(None)

    def should_sell(self, i):
        if self.latest_buy_price is None:
            return False

        if should_realize_profit(self.df_close[i], self.latest_buy_price, self.profit_ratio):
            return True

        if should_stop_loss(self.df_close[i], self.latest_buy_price, self.loss_ratio):
            return True

        return self.add_strategy.should_sell(i)


    def should_buy(self, i):
        if self.latest_buy_price:
            return False

        return self.add_strategy.should_buy(i)

    def set_latest_buy_price(self, buy_price):
        self.latest_buy_price = buy_price
        self.add_strategy.set_latest_buy_price(buy_price)

    def get_latest_buy_price(self):
        return self.latest_buy_price