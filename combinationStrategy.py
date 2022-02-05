class CombinationStrtegy:
    def __init__(self, strategies):
        self.strategies = strategies
        self.set_latest_buy_price(None)

    # ToDo: n個中k個Trueなら、buy等にするか？（複数の指標を目安にできる）
    #       1つがTrueになってから、一定期間内に他の手法の一部(全部)がTrue等
    def should_buy(self, i):
        for strat in self.strategies:
            if strat.should_buy(i):
                return True
        return False

    # ToDo: n個中k個Trueなら、sell等にするか？（複数の指標を目安にできる）
    #       1つがTrueになってから、一定期間内に他の手法の一部(全部)がTrue等
    def should_sell(self, i):
        for strat in self.strategies:
            if strat.should_sell(i):
                return True
        return False

    def set_latest_buy_price(self, buy_price):
        for strat in self.strategies:
            strat.set_latest_buy_price(buy_price)
