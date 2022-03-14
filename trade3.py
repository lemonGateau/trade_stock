import sys
sys.path.append("..")
import os

from pandas_datareader import data
import pandas as pd
from datetime import *
from time import *

from common.print_funcs import *
from common.plot_funcs import *
from common.indicator_funcs import *
from common.util import *
from common.io_data import *

from simulater2 import Simulater

# ImportError: attempted relative import with no known parent package
try:
    from ..indicators import *
except:
    from indicators import *

def main():
    SHORT_TERM       = 12
    LONG_TERM        = 25
    MACD_SIGNAL_TERM = 9
    B_BANDS_TERM     = 25
    ADX_TERM         = 14
    ADXR_TERM        = 25
    MOMENTUM_TERM    = 26
    MOM_SIGNAL_TERM  = 10
    RSI_TERM         = 14

    PROFIT_RATIO     = 0.2
    LOSS_RATIO       = 0.05
    RSI_SELL_RATIO   = 0.8
    RSI_BUY_RATIO    = 0.2

    SYMBOLS = ("BTC-JPY", "ETH-JPY")
    PERIODS = (("10d", "5m"), ("1mo", "15m"), ("4mo", "1h"), ("8y", "1d"), ("10y", "5d"))

    higher = pd.DataFrame()
    lower  = pd.DataFrame()

    for symbol in SYMBOLS:
        for range, interval in PERIODS:
            EXPORT_DIR = f"C:\\Users\\manab\\github_\\trade_stock\\csv_db\\{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            os.mkdir(path = EXPORT_DIR)

            bars = fetch_yahoo_short_bars(symbol, range, interval)
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

            close = bars["Adj Close"]

            bars["sma_short"]   = generate_sma(close, SHORT_TERM)
            bars["sma_long"]    = generate_sma(close, LONG_TERM)
            bars["ema_short"]   = generate_ema(close, SHORT_TERM)
            bars["ema_long"]    = generate_ema(close, LONG_TERM)

            bars["macd"]        = bars["ema_short"] - bars["ema_long"]
            bars["macd_signal"] = generate_sma(bars["macd"], MACD_SIGNAL_TERM)

            sma_cross  = Cross(bars["sma_short"], bars["sma_long"])
            ema_cross  = Cross(bars["ema_short"], bars["ema_long"])
            macd_cross = Cross(bars["macd"]     , bars["macd_signal"])

            sma_cross.set_strategy_name("sma")
            ema_cross.set_strategy_name("ema")
            macd_cross.set_strategy_name("macd")

            bbands2 = BollingerBands(close, B_BANDS_TERM)
            bbands3 = BollingerBands(close, B_BANDS_TERM)

            bbands2.generate_upper(coef=2)
            bbands2.generate_lower(coef=2)
            bbands2.set_strategy_name("bb2")
            bbands3.set_strategy_name("bb3")

            dmi = Dmi(close, bars["High"], bars["Low"], ADX_TERM, ADXR_TERM)
            dmi.compute_tr()
            dmi.compute_dms()
            dmi.compute_dis(ADX_TERM)
            dmi.compute_dx()
            dmi.compute_adx(ADX_TERM)
            dmi.compute_adxr(ADXR_TERM)

            momentum = Momentum()
            momentum.compute_moment(close, MOMENTUM_TERM)
            momentum.generate_signal(MOM_SIGNAL_TERM)
            momentum.generate_baseline(0)

            rsi = Rsi(RSI_SELL_RATIO, RSI_BUY_RATIO)
            rsi.compute_rsi(close, RSI_TERM)

            fp = FinalizedProfit(close, PROFIT_RATIO, LOSS_RATIO)

        # ---------------------------------------------------------------
            # 作戦決定
            strats = (sma_cross, ema_cross, macd_cross, bbands2, bbands3, dmi, momentum, rsi)

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
            #sim.plot_trade_hists(strategies)

            hists   = sim.extract_hists("")
            profits = sim.extract_profits("")

            #print(hists)
            print(profits)

            #hists.to_csv(EXPORT_DIR + "\\hists.csv", index=True)
            profits.to_csv(EXPORT_DIR + "\\profits.csv", index=True)

            higher = pd.concat([higher, profits.head(5)])
            lower  = pd.concat([lower,  profits.tail(5)])

            sleep(15)

        higher.to_csv(EXPORT_DIR + "\\higher" + symbol + ".csv", index=True)
        lower.to_csv(EXPORT_DIR + "\\lower" + symbol + ".csv"  , index=True)

        higher = higher[:0]
        lower  = lower[:0]


if __name__ == '__main__':
    begin_time = time()
    main()
    print(time() - begin_time)
