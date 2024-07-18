import numpy as np


def calc_custom_ema(dataframe, ema_size):
    """
    Function to calculate a dataframe of any size. Does not use TA Lib.
    :param dataframe object of the price data to apply ema to
    :param max_size interger of the size of EMA
    :return dataframe with EMA attached
    """
    ema_name = "ema_" + str(ema_size)
    multiplier = 2 / (ema_size + 1)
    initial_mean = dataframe["close"].head(ema_size).mean()
    for i in range(len(dataframe)):
        if i == ema_size:
            dataframe.loc[i, ema_name] = initial_mean
        elif i > ema_size:
            ema_value = dataframe.loc[i, "close"] * multiplier + dataframe.loc[i-1, ema_name] * (1-multiplier)
            dataframe.loc[i, ema_name] = ema_value
        else:
            dataframe.loc[i, ema_name] = 0.0
    return dataframe
