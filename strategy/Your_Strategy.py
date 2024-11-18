"""
By: LukeLab
Created on 09/20/2023
Version: 1.0
Last Modified: 09/27/2023

Major Updated: 04/04/2024, decision and order function furnish
Still in testing

updated: 04/09/2024, output formatting

# updated: 11/17/2024, final version for open source only
# Version 2.0
# for more info, please visit: https://www.patreon.com/LookAtWallStreet

"""

import yfinance as yf
from moomoo import *
from strategy.Strategy import Strategy
import pandas_ta as pta
from utils.dataIO import read_json_file, write_json_file, logging_info
from utils.time_tool import is_market_hours


class Your_Strategy(Strategy):
    """
    This is an example strategy class, you can define your own strategy here.
    """

    def __init__(self, trader):
        super().__init__(trader)
        self.strategy_name = "Example_Strategy"

        """⬇️⬇️⬇️ Strategy Settings ⬇️⬇️⬇️"""

        self.stock_trading_list = ["SPY", "QQQ"]
        self.trading_qty = {
            # please set the trading quantity for each stock
            "SPY": 88,
            "QQQ": 88
        }

        self.trading_confirmation = True    # True to enable trading confirmation

        # please add any other settings here based on your strategy

        """⬆️⬆️⬆️ Strategy Settings ⬆️⬆️⬆️"""

        print(f"Strategy {self.strategy_name} initialized...")

    def strategy_decision(self):
        print("Strategy Decision running...")
        """ ⬇️⬇️⬇️ Simple Example Strategy starts here ⬇️⬇️⬇️"""
        # please modify the following code to match your own strategy
        for stock in self.stock_trading_list:
            try:
                # 1. get the stock data from quoter, return a pandas dataframe
                df = yf.Ticker(stock).history(interval="1h", actions=False, prepost=False, raise_errors=True)

                # 2. calculate the indicator
                df['fast_ma'] = pta.sma(df['Close'], length=5)
                df['slow_ma'] = pta.sma(df['Close'], length=10)

                price = df['Close'].iloc[-1]
                qty = self.trading_qty[stock]

                # 3. check the signal and place order
                if df["fast_ma"] > df["slow_ma"] and df["fast_ma"].shift(1) <= df["slow_ma"].shift(1):
                    # Buy when the fast MA crosses above the slow MA.
                    print('BUY Signals')
                    self.strategy_make_trade(action='BUY', stock=stock, qty=qty, price=price)   # place order

                if (df["fast_ma"] < df["slow_ma"]) & (df["fast_ma"].shift(1) >= df["slow_ma"].shift(1)):
                    # Sell when the fast MA crosses below the slow MA.
                    print('SELL Signals')
                    self.strategy_make_trade(action='SELL', stock=stock, qty=qty, price=price)  # place order

                time.sleep(1)  # sleep 1 second to avoid the quote limit
            except Exception as e:
                print(f"Strategy Error: {e}")
                logging_info(f'{self.strategy_name}: {e}')

        """ ⏫⏫⏫ Simple Example Strategy ends here ⏫⏫⏫ """

        print("Strategy checked... Waiting next decision called...")
        print('-----------------------------------------------')

    """ ⬇️⬇️⬇️ Order related functions ⬇️⬇️⬇️"""

    def strategy_make_trade(self, action, stock, qty, price):
        if self.trading_confirmation:
            # check if trading confirmation is enabled first
            if action == 'BUY':
                # check the current buying power first
                acct_ret, acct_info = self.trader.get_account_info()
                if acct_ret == RET_OK:
                    current_cash = acct_info['cash']
                else:
                    print('Trader: Get Account Info failed: ', acct_info)
                    return False

                if current_cash > qty * price:
                    # before buy action, check if it has enough cash
                    if is_market_hours():
                        # market order
                        ret, data = self.trader.market_buy(stock, qty, price)
                    else:
                        # limit order for extended hours
                        ret, data = self.trader.limit_buy(stock, qty, price)

                    if ret == RET_OK:
                        # order placed successfully:
                        print(data)
                        self.save_order_history(data)
                        print('make trade success, show latest position:')
                        print(self.get_current_position())  # show the latest position after trade
                    else:
                        print('Trader: Buy failed: ', data)
                        logging_info(f'{self.strategy_name}: Buy failed: {data}')
                else:
                    print('Trader: Buy failed: Not enough cash to buy')
                    logging_info(f'{self.strategy_name}: Buy failed: Not enough cash to buy')

            if action == 'SELL':
                position_data = self.get_current_position()
                if not position_data:
                    # check current position first
                    return False

                if qty <= position_data[stock]["qty"]:
                    # before sell action, check if it has enough position to sell
                    if is_market_hours():
                        # market order
                        ret, data = self.trader.market_sell(stock, qty, price)
                    else:
                        # limit order for extended hours
                        ret, data = self.trader.limit_sell(stock, qty, price)
                    if ret == RET_OK:
                        print(data)
                        logging_info(f'{self.strategy_name}: {data}')
                        self.save_order_history(data)
                        print('make trade success, show latest position:')
                        print(self.get_current_position())  # show the latest position after trade
                    else:
                        print('Trader: Sell failed: ', data)
                        logging_info(f'{self.strategy_name}: Sell failed: {data}')
                else:
                    print('Trader: Sell failed: Not enough position to sell')
                    logging_info(f'{self.strategy_name}: Sell failed: Not enough position to sell')

    def save_order_history(self, data):
        file_data = read_json_file("order_history.json")
        data_dict = data.to_dict()
        new_dict = {}
        for key, v in data_dict.items():
            new_dict[key] = v[0]
        logging_info(f'{self.strategy_name}: {str(new_dict)}')

        if file_data:
            file_data.append(new_dict)
        else:
            file_data = [new_dict]
        write_json_file("order_history.json", file_data)

    # add any other functions you need here
