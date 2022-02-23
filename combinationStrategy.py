from collections import OrderedDict
from common.plot_funcs import plot_df


class CombinationStrategy:
    def __init__(self, buy_strategies, sell_strategies):
        # 深いコピー
        self.strategies = buy_strategies + sell_strategies
        # 重複要素削除
        self.strategies = list(OrderedDict.fromkeys(self.strategies))

        self.buy_strats  = buy_strategies
        self.sell_strats = sell_strategies

        self.set_latest_buy_price(None)
        self.set_strategy_name()

    def should_buy(self, i):
        for strat in self.buy_strats:
            if strat.should_buy(i):
                # print(strat.get_strategy_name(), end="※ ")
                return True
        return False

    def should_sell(self, i):
        for strat in self.sell_strats:
            if strat.should_sell(i):
                # print(strat.get_strategy_name(), end="※ ")
                return True
        return False

    def set_strategy_name(self, strat_names=None):
        if type(strat_names) is str:
            self.strat_name = strat_names
            return

        if strat_names:
            self.strat_name = '_'.join(strat_names)
            return

        buy_strat_names  = []
        for strat in self.buy_strats:
            buy_strat_names.append(strat.get_strategy_name())

        sell_strat_names = []
        for strat in self.sell_strats:
            sell_strat_names.append(strat.get_strategy_name())

        self.strat_name = '_'.join(buy_strat_names) + '--' + '_'.join(sell_strat_names)


    def get_strategy_name(self):
        return self.strat_name


    def set_latest_buy_price(self, buy_price):
        for strat in self.strategies:
            strat.set_latest_buy_price(buy_price)

    def build_df_indicator(self):
        dfs = []
        for strat in self.strategies:
            df = strat.build_df_indicator()
            dfs.append(df)

        return dfs

    def plot_df_indicator(self):
        plot_df(self.build_df_indicator())
