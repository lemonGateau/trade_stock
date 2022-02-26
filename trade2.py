import sys
sys.path.append("..")
import os

from pandas_datareader import data
import pandas as pd
from datetime import *

from common.print_funcs import *
from common.profit_funcs import *
from common.plot_funcs import  plot_df
from common.indicator_funcs import *

from util import *
from io_data import *
from simulater import *

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
    RSI_SELL_RATIO   = 0.7
    RSI_BUY_RATIO    = 0.3

    symbol = "BTC-JPY"

    # 日足より短
    RANGE    = "7d"
    INTERVAL = "5m"

    bars = fetch_yahoo_short_bars(symbol, RANGE, INTERVAL)
    begin = bars.index[0]
    end   = bars.index[-1]

    """
    # 日足以上長
    SOURCE  = "yahoo"
    begin = datetime(2017, 1, 1)
    end   = datetime.today()

    bars = data.DataReader(symbol, SOURCE, begin, end)
    """

    close = bars["Adj Close"]

    # 取引戦略
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

    bbands2.set_upper(coef=2)
    bbands2.set_lower(coef=2)
    bbands2.set_strategy_name("bb2")
    bbands3.set_strategy_name("bb3")

    dmi = Dmi(close, bars["High"], bars["Low"], ADX_TERM, ADXR_TERM)

    momentum = Momentum()
    momentum.compute_moment(close, MOMENTUM_TERM)
    momentum.generate_signal(MOM_SIGNAL_TERM)
    momentum.generate_baseline(0)

    rsi = Rsi(RSI_SELL_RATIO, RSI_BUY_RATIO)
    rsi.compute_rsi(close, RSI_TERM)

    fp = FinalizedProfit(close, PROFIT_RATIO, LOSS_RATIO)

    dmi_bar = dmi.build_df_indicator()
    bb2_bar = bbands2.build_df_indicator()
    bb3_bar = bbands3.build_df_indicator()
    mom_bar = momentum.build_df_indicator()
    rsi_bar = rsi.build_df_indicator()

    bars = pd.concat([bars, dmi_bar, bb2_bar, bb3_bar, mom_bar, rsi_bar], axis=1)
    bars = bars.loc[:, ~bars.columns.duplicated()]    # 重複列を削除

    SAVE_DIR = f"C:\\Users\\manab\\github_\\trade_stock\\csv_files\\{datetime.now().strftime('%Y%m%d_%H%M')}"
    os.mkdir(path = SAVE_DIR)

    bars.to_csv(SAVE_DIR + "\\bars.csv", index=True, encoding="utf-8")

# ---------------------------------------------------------------
    # シミュレーション
    print_simulation_conditions(symbol, begin, end)

    strats = (sma_cross, ema_cross, macd_cross, bbands2, bbands3, dmi, momentum, rsi)
    """
    data = pd.DataFrame(data=close, index=bars.index)

    for strat in strats:
        result = simulate_trade(strat, bars.index, close)
        data = pd.concat([data, result], axis=1)

    results = data.loc[:, ~data.columns.duplicated()]
    """

    results = simulate_grand_trade(strats, bars.index, close, [], [])

    results.to_csv(SAVE_DIR + "\\orders.csv", index=True, encoding="utf-8")

# ---------------------------------------------------------------
    # 利益計算
    profits    = []
    bid_counts = []
    ask_counts = []

    for col in results.columns.values[1:]:
        bids = results.loc[results[col] == "bid", ["Adj Close", col]]
        asks = results.loc[results[col] == "ask", ["Adj Close", col]]

        bid_counts.append(len(bids.index))
        ask_counts.append(len(asks.index))

        profits.append(int(sum(asks["Adj Close"]) - sum(bids["Adj Close"][:len(asks.index)])))

    d = pd.DataFrame(data={"profit": profits, "bid_count": bid_counts, "ask_count": ask_counts},\
         index=results.columns.values[1:])

    sorted = d.sort_values(by="profit", ascending=False)

    # print_extract_strats_df(d, "", "dmi")
    # print_extract_strats_df(d, "dmi", "")

    sorted.to_csv(SAVE_DIR + "\\profits.csv", index=True, encoding="utf-8")

# ---------------------------------------------------------------
    # プロット
    # for strat in strats:
        # strat.plot_df_indicator()




if __name__ == '__main__':
    main()

