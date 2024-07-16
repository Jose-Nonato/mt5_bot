import json
import os
import mt5_lib


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


if __name__ == "__main__":
    project_settings = get_project_settings("project_settings.json")
    start = start_up(project_settings)
