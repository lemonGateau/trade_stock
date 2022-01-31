class FinalizedProfit:
    def __init__(self, profit_ratio, loss_ratio):
        self.profit_ratio = profit_ratio
        self.loss_ratio   = loss_ratio

    def should_sell(self, latest_price):
        pass

    def should_buy(self, latest_price):
        pass
