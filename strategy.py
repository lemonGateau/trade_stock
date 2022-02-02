from this import d


class Strategy:
    def __init__(self):
        pass

    def should_buy(self, i):
        pass

    def should_sell(self, i):
        pass

    def set_latest_buy_price(self, buy_price):
        self.latest_buy_price = buy_price

    def get_latest_buy_price(self):
        return self.latest_buy_price

