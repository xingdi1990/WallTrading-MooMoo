# from discord_notification.discord_notify_webhook import send_webhook_message
from utils.dataIO import get_current_time, logging_info
# from utils.send_email import send_emails
from moomoo import *


class Strategy:
    """
    You may not need to modify this class,
    just inherit it and overwrite the strategy_decision() function
    in your own strategy class, eg: Your_Strategy(Strategy)
    """

    def __init__(self, trader):
        # define your own strategy name
        self.strategy_name = "strategy template class"
        self.trader = trader
        self.strategy_load_notification()

    # ******
    # Functions below need to overwrite in your own strategy class
    def strategy_decision(self):
        pass

    # ******
    # Functions below do not need to be modified, free to check and call
    def strategy_load_notification(self):
        print(f"{self.strategy_name}: Strategy Loaded and Running")
        # OR, add any code you want to run when the strategy is loaded
        pass

    def update_strategy_status(self):
        # update the strategy status after each run
        # please implement this function based on your own strategy
        pass

    def send_notification_via_email(self, msg_body):
        """
        please uncomment the following line and fill the parameters to send email
        """
        # send_emails(from_, to, bcc: list, msg_subject, msg_body, login_email, login_password)
        # print(f"Strategy: {self.strategy_name} Status: Email sent")
        # logging_info(f"Strategy: {self.strategy_name} Status: Email sent")
        pass

    def send_notification_via_discord(self, msg_body):
        """
        please uncomment the following line and fill the parameters to send discord message
        """
        # send a message to a Discord channel via webhook
        # send_webhook_message(msg_body)
        # print(f"Strategy: {self.strategy_name} Status: Discord msg sent")
        # logging_info(f"Strategy: {self.strategy_name} Status: Discord msg sent")
        pass

    def get_current_position(self):
        position_ret, position_data = self.trader.get_positions()
        if position_ret != RET_OK:
            # get current position quantity
            print(f'{get_current_time()}Trader: MooMoo API error, Please Check')
            logging_info(f'{get_current_time()}Trader: MooMoo API error, Please Check')
            return False
        return position_data
