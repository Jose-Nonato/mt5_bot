import mt5_lib
import indicator_lib


def ema_cross_strategy(symbol, timeframe, ema_one, ema_two):
    """
    Function wich runs the EMA Cross Strategy.
    :param symbol string of symbol to be quired
    :param timeframe string of timeframe to be quired
    :param ema_one integer of the lowest timeframe length for EMA
    :param ema_two integet of the highest timeframe length for EMA
    :return trade event dataframe
    """
    data = get_data(symbol, timeframe)
    data = calc_indicators(data, ema_one, ema_two)
    data = det_trade(data, ema_one, ema_two)
    return data


def get_data(symbol, timeframe):
    data = mt5_lib.get_candlesticks(symbol, timeframe, 1000)
    return data


def calc_indicators(data, ema_one, ema_two):
    dataframe = indicator_lib.calc_custom_ema(data, ema_one)
    dataframe = indicator_lib.calc_custom_ema(dataframe, ema_two)
    dataframe = indicator_lib.ema_cross_calculator(dataframe, ema_one, ema_two)
    return dataframe


def det_trade(data, ema_one, ema_two):
    ema_one_column = "ema_" + str(ema_one)
    ema_two_column = "ema_" + str(ema_two)
    if ema_one > ema_two:
        ema_column = ema_one_column
        min_value = ema_one
    elif ema_two > ema_one:
        ema_column = ema_two_column
        min_value = ema_two
    else:
        raise ValueError("EMA value are the same!")
    
    dataframe = data.copy()
    dataframe["take_profit"] = 0.00
    dataframe["stop_price"] = 0.00
    dataframe["stop_loss"] = 0.00
    
    for i in range(len(dataframe)):
        if i <= min_value:
            continue
        else:
            if dataframe.loc[i, "ema_cross"]:
                if dataframe.loc[i, "open"] > dataframe.loc[i, "close"]:
                    stop_loss = dataframe.loc[i, ema_column]
                    stop_price = dataframe.loc[i,"high"]
                    distance = stop_price - stop_loss
                    take_profit = stop_price + distance
                else:
                    stop_loss = dataframe.loc[i, ema_column]
                    stop_price = dataframe.loc[i, "low"]
                    distance = stop_loss - stop_price
                    take_profit = stop_price - distance
                dataframe.loc[i, "stop_loss"] = stop_loss
                dataframe.loc[i, "stop_price"] = stop_price
                dataframe.loc[i, "take_profit"] = take_profit

    return dataframe