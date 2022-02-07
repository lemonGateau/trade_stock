from plot_funcs import plot_df


class CombinationStrategy():
    def __init__(self, strategies):
        self.strategies = strategies

        self.set_latest_buy_price(None)
        self.set_strategy_name()

    # ToDo: n個中k個Trueなら、buy等にするか？（複数の指標を目安にできる）
    #       1つがTrueになってから、一定期間内に他の手法の一部(全部)がTrue等
    def should_buy(self, i):
        for strat in self.strategies:
            if strat.should_buy(i):
                # print(strat.get_strategy_name(), end="※ ")
                return True
        return False

    # ToDo: n個中k個Trueなら、sell等にするか？（複数の指標を目安にできる）
    #       1つがTrueになってから、一定期間内に他の手法の一部(全部)がTrue等
    def should_sell(self, i):
        for strat in self.strategies:
            if strat.should_sell(i):
                # print(strat.get_strategy_name(), end="※ ")
                return True
        return False

    def set_latest_buy_price(self, buy_price):
        for strat in self.strategies:
            strat.set_latest_buy_price(buy_price)

    def set_strategy_name(self, strat_names=None):
        if type(strat_names) is str:
            self.strat_name = strat_names
            return

        if strat_names is None:
            strat_names = []
            for strat in self.strategies:
                strat_names.append(strat.get_strategy_name())

        self.strat_name = '_'.join(strat_names)

    def get_strategy_name(self):
        return self.strat_name

    def build_df_indicator(self):
        dfs = []
        for strat in self.strategies:
            df = strat.build_df_indicator()
            dfs.append(df)

        return dfs

    def plot_df_indicator(self):
        plot_df(self.build_df_indicator())
