import sys
sys.path.append("..")
import os

from pandas_datareader import data
import pandas as pd
from datetime import *
from time import time

from common.print_funcs import *
from common.util import *
from common.io_data import *
import config as conf

from simulater2 import Simulater

# ImportError: attempted relative import with no known parent package
try:
    from ..indicators import *
except:
    from indicators import *

def main():
    EXPORT_DIR = f"C:\\Users\\manab\\github_\\trade_stock\\csv_db\\{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.mkdir(path = EXPORT_DIR)

    """
    RANGES    = ("10d", "30d", "100d")
    INTERVALS = ("5m" , "15m", "1h")
    """

    symbol = "BTC-JPY"
    #symbol = "ETH-JPY"


    # 日足より短
    RANGE    = "3d"
    INTERVAL = "5m"

    bars = fetch_yahoo_short_bars(symbol, RANGE, INTERVAL)
    BEGIN = bars.index[0]
    END   = bars.index[-1]

    """
    # 日足以上長
    SOURCE  = "yahoo"
    BEGIN = datetime(2022, 1, 1)
    END   = datetime.today()

    bars = data.DataReader(symbol, SOURCE, BEGIN, END)
    """

    print_reference_data_period(symbol, BEGIN, END)

    close = bars["Adj Close"]

    cross_sma = CrossSma()
    cross_ema = CrossEma()
    cross_macd = CrossMacd()

    cross_sma.generate_smas(close, [conf.SHORT_TERM, conf.LONG_TERM])
    cross_ema.generate_emas(close, [conf.SHORT_TERM, conf.LONG_TERM])
    cross_macd.generate_macds(close, [conf.SHORT_TERM, conf.LONG_TERM], conf.MACD_SIGNAL_TERM)

    bbands2 = BollingerBands(close, conf.BB_TERM)
    bbands2.generate_upper(coef=2)
    bbands2.generate_lower(coef=2)

    bbands3 = BollingerBands(close, conf.BB_TERM)

    bbands2.set_strategy_name("bb2")
    bbands3.set_strategy_name("bb3")

    dmi = Dmi()
    dmi.compute_tr(close, bars["High"], bars["Low"])
    dmi.compute_dms(bars["High"], bars["Low"])
    dmi.compute_dis(conf.ADX_TERM)
    dmi.compute_dx()
    dmi.compute_adx(conf.ADX_TERM)
    dmi.compute_adxr(conf.ADXR_TERM)

    momentum = Momentum()
    momentum.compute_moment(close, conf.MOM_TERM)
    momentum.generate_signal(conf.MOM_SIGNAL_TERM)
    momentum.generate_baseline(0)

    rsi = Rsi(conf.RSI_SELL_RATIO, conf.RSI_BUY_RATIO)
    rsi.compute_rsi(close, conf.RSI_TERM)

    fp = FinalizedProfit(close, conf.PROFIT_RATIO, conf.LOSS_RATIO)


    """
    dmi_bar = dmi.build_df_indicator()
    bb2_bar = bbands2.build_df_indicator()
    bb3_bar = bbands3.build_df_indicator()
    mom_bar = momentum.build_df_indicator()
    rsi_bar = rsi.build_df_indicator()

    bars = pd.concat([bars, dmi_bar, bb2_bar, bb3_bar, mom_bar, rsi_bar], axis=1)
    bars = bars.loc[:, ~bars.columns.duplicated()]    # 重複列を削除

    bars.to_csv(EXPORT_DIR + "\\bars.csv", index=True, encoding="utf-8")
    """

# ---------------------------------------------------------------
    # 作戦決定
    strats = (cross_sma, cross_ema, cross_macd, bbands2, bbands3, dmi, momentum, rsi)

    comb_strats = []
    for bid_strat in strats:
        for ask_strat in strats:
            comb_strats.append(CombinationStrategy([bid_strat], [ask_strat]))
            comb_strats.append(CombinationStrategy([bid_strat], [ask_strat, fp]))


    #strategies = strats
    strategies = comb_strats


# ToDo: 実行速度短縮 & sim._simulate_trade(strat)を繰り返すべきか？
# ---------------------------------------------------------------
    # シミュレーション
    sim = Simulater(close.index, close)

    sim.simulate_strats_trade(strategies)
    sim.compute_profits()

    hists   = sim.extract_hists("")
    profits = sim.extract_profits("")

    #print(hists)
    print(profits)

    hists.to_csv(EXPORT_DIR + "\\histories.csv", index=True)
    profits.to_csv(EXPORT_DIR + "\\profits.csv", index=True)

    sim.plot_trade_hists(strategies)



if __name__ == '__main__':
    begin_time = time()
    main()
    print(time() - begin_time)
