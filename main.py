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


def run_strategy(project_settings, symbol):
    timeframe = project_settings["mt5"]["timeframe"]
    orders = mt5_lib.get_all_open_orders()
    for order in orders:
        mt5_lib.cancel_order(order)
    for symbol in symbols:
        # candlesticks = mt5_lib.get_candlesticks(symbol, timeframe, 1000)
        comment_string = f"EMA_Cross_strategy_{symbol}"
        mt5_lib.cancel_filtered_orders(symbol, comment_string)
        data = ema_cross_strategy.ema_cross_strategy(symbol, timeframe, 50, 200, 1000, 0.01)
    return True


if __name__ == "__main__":
    project_settings = get_project_settings("project_settings.json")
    start = start_up(project_settings)
    symbols = project_settings["mt5"]["symbols"]

    if start:
        current_time = 0
        previous_time = 0
        timeframe = project_settings["mt5"]["timeframe"]
        while 1:
            time_candle = mt5_lib.get_candlesticks("USDJPY", timeframe, 1)
            current_time = time_candle["time"][0]
            print(current_time != previous_time, current_time, previous_time)
            if current_time != previous_time:
                print("New Candle! Let's trade.")
                previous_time = current_time
                strategy = run_strategy(project_settings, symbols)
            else:
                print("No new candle. Sleeping!")
                time.sleep(1)
