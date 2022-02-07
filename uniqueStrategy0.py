from combinationStrategy import CombinationStrategy


class UniqueStrategy0(CombinationStrategy):
    def __init__(self, entry_strategies, exit_strategies, entry_side="buy"):
        if entry_side == "buy":
            self.buy_strats = entry_strategies
            self.sell_strats = exit_strategies
        elif entry_side == "sell":
            self.buy_strats = exit_strategies
            self.sell_strats  = entry_strategies
        else:
            raise Exception

        self.entry_side = entry_side
        self.set_latest_entry_price(None)
        self.set_strategy_name("u1")    # ToDo: entryとexitから命名

    def should_buy(self, i):
        if is_entryed():
            pass
