import numpy as np

def generate_sma(df_prices=[], window=5):
    return df_prices.rolling(window).mean()

def generate_ema(df_prices=[], span=5):
    return df_prices.ewm(span).mean()


def is_crossover(ma1_list, ma2_list):
    ''' 交差判定(直近値で ma1 が ma2 を上回るか) '''
    if (len(ma1_list) < 2) or (len(ma1_list) < 2):
        return False


    with np.errstate(invalid='ignore'): # nanの比較によるエラーを防ぐ
        return (ma1_list[-2] < ma2_list[-2]) and (ma1_list[-1] >= ma2_list[-1])


def should_realize_profit(latest_price, buy_price, profit_ratio=0.1):
    ''' 利確判定 '''
    return (latest_price > (buy_price * (1.0 + profit_ratio)))

def should_stop_loss(latest_price, buy_price, loss_ratio=0.05):
    ''' 損切り判定 '''
    return (latest_price < (buy_price * (1.0 - loss_ratio)))
