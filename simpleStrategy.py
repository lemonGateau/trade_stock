from print_funcs import *

class SimpleStrategy:
    def __init__(self, profit_ratio=0.2, loss_ratio=0.1):
        self.profit_ratio = profit_ratio
        self.loss_ratio   = loss_ratio
        self.set_buy_price(None)

    def realize_trade(self, latest_price):
        if self.buy_price is None:
            return

        if latest_price > self.buy_price * (1.0 + self.profit_ratio):
            self.sell(latest_price)
        elif latest_price < self.buy_price * (1.0 - self.loss_ratio):
            self.sell(latest_price)

    def sell(self, sell_price):
        if self.buy_price:
            print("sell: ", end="")
            print_prices([sell_price, self.buy_price])
            self.set_buy_price(None)

    def buy(self, buy_price):
        if self.buy_price is None:
            print("buy : ", end="")
            print_prices([buy_price])
            self.set_buy_price(buy_price)

    def set_buy_price(self, buy_price):
        self.buy_price = buy_price

    def get_buy_price(self):
        return self.buy_price
