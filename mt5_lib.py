import MetaTrader5


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
