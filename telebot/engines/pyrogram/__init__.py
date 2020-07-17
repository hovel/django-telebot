import json


class Engine(AbstractEngine):
    
    def __init__(self, bot: Bot):
        if not bot.token:
            raise TypeError('Token for Telegram bot must be non-empty string value') 
        self.bot = TGBot(bot.token)
        super().__init__(bot)

    def _send_message(self, link, message: str, kwgs: dict=None) -> bool:
        log_partial = partial(log_message, user_link=link, direction=FROM_BOT, message=message, addional_info=json.dumps(kwargs))
        pass