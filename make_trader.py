import mt5_lib
import helper_functions

def make_trade(balance, comment, amount_to_risk, symbol, take_profit, stop_loss, stop_price):
    """
    Function to make a trade once a price signal is retrieved
    """
    balance = float(balance)
    balance = round(balance, 2)
    take_profit = float(take_profit)
    take_profit = round(take_profit, 4)
    stop_loss = float(stop_loss)
    stop_loss = round(stop_loss, 4)
    stop_price = float(stop_price)
    stop_price = round(stop_price, 4)

    lot_size = helper_functions.calc_lot_size(balance, amount_to_risk, stop_loss, stop_price, symbol)

    if stop_price > stop_loss:
        trade_type = "BUY_STOP"
    else:
        trade_type = "SELL_STOP"

    trade_outcome = mt5_lib.place_order(trade_type, symbol, lot_size, stop_loss, stop_price, take_profit, comment, False)

    return trade_outcome