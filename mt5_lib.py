import MetaTrader5
import pandas as pd


def start_mt5(project_settings):
    """
    Function to start MetaTrader5
    :return: Boolean: True = Started, False = not Started
    """
    username = int(project_settings['mt5']['username'])
    password = project_settings['mt5']['password']
    server = project_settings['mt5']['server']
    mt5_pathway = project_settings['mt5']['mt5_pathway']

    mt5_init = False
    try:
        mt5_init = MetaTrader5.initialize(
            login=username,
            password=password,
            server=server
        )
    except Exception as e:
        print(f'Error initializing Metatrader5: {e}')
        mt5_init = False

    mt5_login = False
    if mt5_init:
        try:
            mt5_login = MetaTrader5.login(
                login=username,
                password=password,
                server=server
            )
        except Exception as e:
            print(f'Error logging into Metatrader5: {e}')
            mt5_login = False

    if mt5_login:
        return True
    return False


def initialize_symbol(symbol):
    """
    Function to initialize symbol on MT5. Assumes that MT5 is already initialized.
    :param symbol: string of symbol.
    :return: Boolean: True = Initialized, False = not Initialized
    """
    all_symbols = MetaTrader5.symbols_get()
    symbols_name = []
    for sym in all_symbols: 
        symbols_name.append(sym.name)
    if symbol in symbols_name:
        try:
            MetaTrader5.symbol_select(symbol, True)
            return True
        except Exception as e:
            print(f"Error enabling {symbol}. Error: {e}")
            return False
    else:
        print(f"Symbol {symbol} does not exists on this version of MT5.")
        return False


def get_candlesticks(symbol, timeframe, number_of_candles):
    """
    Function to query historic candlesticks data from MT5
    :param symbol: string of the symbol being retrieved
    :param timeframe: string of the timeframe being retrieved
    :param number_of_candles: interger of number of candles to retrieve. Limited to 50.000
    :return dataframe of candlesticks
    """
    if number_of_candles > 50000:
        raise ValueError("No more than 50000 candles can be retrieved at this time")
    mt5_timeframe = set_query_timeframe(timeframe)
    candles = MetaTrader5.copy_rates_from_pos(symbol, mt5_timeframe, 1, number_of_candles)
    dataframe = pd.DataFrame(candles)
    return dataframe


def set_query_timeframe(timeframe):
    """
    Function to implement a conversion from a user-friendly timeframe string into a MT5 friendly object
    :param timeframe: string of the timeframe
    :return MT5 Timeframe Object
    """
    if timeframe == "M1":
        return MetaTrader5.TIMEFRAME_M1
    elif timeframe == "M2":
        return MetaTrader5.TIMEFRAME_M2
    elif timeframe == "M3":
        return MetaTrader5.TIMEFRAME_M3
    elif timeframe == "M4":
        return MetaTrader5.TIMEFRAME_M4
    elif timeframe == "M5":
        return MetaTrader5.TIMEFRAME_M5
    elif timeframe == "M6":
        return MetaTrader5.TIMEFRAME_M6
    elif timeframe == "M10":
        return MetaTrader5.TIMEFRAME_M10
    elif timeframe == "M12":
        return MetaTrader5.TIMEFRAME_M12
    elif timeframe == "M15":
        return MetaTrader5.TIMEFRAME_M15
    elif timeframe == "M20":
        return MetaTrader5.TIMEFRAME_M20
    elif timeframe == "M30":
        return MetaTrader5.TIMEFRAME_M30
    elif timeframe == "H1":
        return MetaTrader5.TIMEFRAME_H1
    elif timeframe == "H2":
        return MetaTrader5.TIMEFRAME_H2
    elif timeframe == "H3":
        return MetaTrader5.TIMEFRAME_H3
    elif timeframe == "H4":
        return MetaTrader5.TIMEFRAME_H4
    elif timeframe == "H6":
        return MetaTrader5.TIMEFRAME_H6
    elif timeframe == "H8":
        return MetaTrader5.TIMEFRAME_H8
    elif timeframe == "H12":
        return MetaTrader5.TIMEFRAME_H12
    elif timeframe == "D1":
        return MetaTrader5.TIMEFRAME_D1
    elif timeframe == "W1":
        return MetaTrader5.TIMEFRAME_W1
    elif timeframe == "MN1":
        return MetaTrader5.TIMEFRAME_MN1
    else:
        print(f"Incorrect timeframe provided. {timeframe}")
        raise ValueError