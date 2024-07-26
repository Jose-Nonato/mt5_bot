import json
import os, time
import mt5_lib, indicator_lib, ema_cross_strategy


def get_project_settings(filepath):
    if os.path.exists(filepath):
        f = open(filepath, 'r')
        data_user = json.load(f)
        f.close()
        return data_user
    else:
        raise ImportError("filepath doesn't exist")


def start_up(project_settings):
    """
    Function to start up procedures for App. Includes starting/testing initializing symbols and anything else to ensure
    app start is succesfully launched.
    :param project_settings: json object of the project settings
    :return: Boolean. True if app start is successfully launched, otherwise False
    """
    startup = mt5_lib.start_mt5(project_settings)
    if startup:
        print("MetaTrader startup succesfully!")
        symbols = project_settings["mt5"]["symbols"]
        for symbol in symbols:
            outcome = mt5_lib.initialize_symbol(symbol)
            if outcome is True:
                print(f"{symbol} initialized!")
            else:
                raise Exception(f"{symbol} not initialized")
        return True
    return False


def run_strategy(project_setting):
    symbols = project_settings["mt5"]["symbols"]
    timeframe = project_settings["mt5"]["timeframe"]
    for symbol in symbols:
        candlesticks = mt5_lib.get_candlesticks(symbol, timeframe, 1000)
        data = ema_cross_strategy.ema_cross_strategy(symbol, timeframe, 50, 200, 1000, 0.01)
    return True


if __name__ == "__main__":
    project_settings = get_project_settings("project_settings.json")
    start = start_up(project_settings)

    if start:
        current_time = 0
        previous_time = 0
        timeframe = project_settings["mt5"]["timeframe"]
        while 1:
            time_candle = mt5_lib.get_candlesticks("BTCUSD.a", timeframe, 1)
            current_time = time_candle["time"][0]
            if current_time != previous_time:
                previous_time = current_time
                strategy = run_strategy(project_settings)
    else:
        time.sleep(1)
