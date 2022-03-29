import sys
from textwrap import shorten
sys.path.append("..")
import os

from pandas_datareader import data
import pandas as pd
from datetime import *
from time import *

from common.print_funcs import *
from common.util import *
from common.io_data import *
import config as conf

from simulater2 import Simulater

# ImportError: attempted relative import with no known parent package
try:
    from ..indicators import *
    from ..yahoo_finance import YahooFinance
except:
    from indicators import *
    from yahoo_finance import YahooFinance

def main():
    SYMBOLS = ("BTC-JPY", "ETH-JPY")
    PERIODS = (("10d", "5m"), ("1mo", "15m"), ("4mo", "1h"), ("8y", "1d"), ("10y", "5d"))

    higher = pd.DataFrame()
    lower  = pd.DataFrame()

    for symbol in SYMBOLS:
        for range, interval in PERIODS:
            EXPORT_DIR = f"C:\\Users\\manab\\github_\\trade_stock\\csv_db\\{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            os.mkdir(path = EXPORT_DIR)

            yahoo = YahooFinance(symbol)
            bars = yahoo.generate_ohlc(range, interval)

            BEGIN = bars.index[0]
            END   = bars.index[-1]

            """
            # 日足以上長
            SOURCE  = "yahoo"
            BEGIN = datetime(2022, 1, 1)
            END   = datetime.today()

            bars = data.DataReader(symbol, SOURCE, BEGIN, END)
            """

            print_reference_data_period(symbol, BEGIN, END, range, interval)

            close = bars["Close"]

            cross_sma  = CrossSma()
            cross_ema  = CrossEma()
            cross_macd = CrossMacd()
            cross_sma.generate_indicators(close , [conf.SHORT_TERM, conf.LONG_TERM])
            cross_ema.generate_indicators(close , [conf.SHORT_TERM, conf.LONG_TERM])
            cross_macd.generate_indicators(close, [conf.SHORT_TERM, conf.LONG_TERM], conf.MACD_SIGNAL_TERM)

            bbands2 = BollingerBands(close)
            bbands2.generate_indicators(conf.BB_TERM, coef=2)
            bbands2.set_strategy_name("bb2")

            bbands3 = BollingerBands(close)
            bbands3.generate_indicators(conf.BB_TERM, coef=3)
            bbands3.set_strategy_name("bb3")

            dmi = Dmi()
            dmi.generate_indicators(close, bars["High"], bars["Low"], [conf.ADX_TERM, conf.ADXR_TERM])

            momentum = Momentum()
            momentum.generate_indicators(close, [conf.MOM_TERM, conf.MOM_SIGNAL_TERM], base_value=0)

            rsi = Rsi()
            rsi.generate_indicators(close, conf.RSI_TERM, conf.RSI_SELL_RATIO, conf.RSI_BUY_RATIO)

            fp = FinalizedProfit(close)
            fp.generate_indicators(conf.PROFIT_RATIO, conf.LOSS_RATIO)

        # ---------------------------------------------------------------
            # 作戦決定
            strats = (cross_sma, cross_ema, cross_macd, bbands2, bbands3, dmi, momentum, rsi)

            comb_strats = []
            for bid_strat in strats:
                for ask_strat in strats:
                    comb_strats.append(CombinationStrategy([bid_strat], [ask_strat]))
                    comb_strats.append(CombinationStrategy([bid_strat], [ask_strat, fp]))

            strategies = comb_strats

            # シミュレーション
            sim = Simulater(close.index, close)

            sim.simulate_strats_trade(strategies)
            sim.compute_profits()

            #hists   = sim.extract_hists("")
            profits = sim.extract_profits("")

            #print(hists)
            print(profits)

            #hists.to_csv(EXPORT_DIR + "\\hists.csv", index=True)
            profits.to_csv(EXPORT_DIR + "\\profits.csv", index=True)

            higher = pd.concat([higher, profits.head(5)])

            #sim.plot_trade_hists(strategies)

            sleep(5)


        higher.to_csv(EXPORT_DIR + "\\higher" + symbol + ".csv", index=True)

        higher = higher[:0]





if __name__ == '__main__':
    begin_time = time()
    main()
    print(time() - begin_time)
