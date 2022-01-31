

def generate_sma(df_prices=[], window=5):
    return df_prices.rolling(window).mean()

def generate_ema(df_prices=[], span=5):
    return df_prices.ewm(span).mean()


def is_crossover(ma1_list, ma2_list):
    ''' 直近値で ma1 が ma2 を上回るか '''
    if (len(ma1_list) < 2) or (len(ma1_list) < 2):
        return False

    if (ma1_list[-2] < ma2_list[-2]) and (ma1_list[-1] >= ma2_list[-1]):
        return True

    return False
