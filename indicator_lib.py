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


def ema_cross_calculator(dataframe, ema_one, ema_two):
    """
    Function to calculate on EMA cross event.
    :param dataframe: dataframe object
    :param ema_one: integer of EMA 1 size
    :param ema_two: interget of EMA 2 size
    :return dataframe with cross event
    """
    ema_one_column = "ema_" + str(ema_one)
    ema_two_column = "ema_" + str(ema_two)

    dataframe['position'] = dataframe[ema_one_column] > dataframe[ema_two_column]
    dataframe['pre_position'] = dataframe['position'].shift(1)
    dataframe.dropna(inplace=True)
    dataframe['ema_cross'] = np.where(dataframe['position'] == dataframe['pre_position'], False, True)
    dataframe = dataframe.drop(columns="position")
    dataframe = dataframe.drop(columns="pre_position")
    return dataframe
