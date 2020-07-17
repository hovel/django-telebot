import json
from traceback import format_exc
from functools import partial, singledispatchmethod
from telegram import Bot as TGBot
from telegram.error import (TelegramError, Unauthorized, BadRequest, 
                            TimedOut, ChatMigrated, NetworkError)

from telebot.base.models import Bot, User, UserLink
from telebot.engines.base import AbstractEngine
from telebot.helpers import log_message, FROM_BOT



class Engine(AbstractEngine):
    
    def __init__(self, bot: Bot):
        if not bot.token:
            raise TypeError('Token for Telegram bot must be non-empty string value') 
        self.bot = TGBot(bot.token)
        super().__init__(bot)

    def _send_message(self, link, message: str, kwgs: dict=None) -> bool:
        if kwgs is None:
            kwgs = {}
        log_partial = partial(log_message, user_link=link, direction=FROM_BOT, message=message, addional_info=json.dumps(kwgs))
        if not link.active:
            log_partial(success=False, error='UserLink not active')
        try:
            message = self.bot.send_message(link.chat_id, message, **kwgs)
        except Unauthorized:
            link.active = False
            link.save()
            log_partial(success=False, error='Unauthorized')
            return False
        except BadRequest:
            log_partial(success=False, error=f'Bad Request {format_exc()}')
            return False
        except TimedOut:
            log_partial(success=False, error='Timeout')
            return False
        except NetworkError:
            log_partial(success=False, error='NetworkError')
            return False
        except ChatMigrated as e:
            link.chat_id = e.new_chat_id
            link.save()
            log_partial(success=False, error='ChatMigrated')
            return False
        except TelegramError:
            log_partial(success=False, error=f'Telegram Error {format_exc()}')
            return False
        if not message:
            log_partial(success=False, error=f'No message delivered by unknown reason')
        log_partial(success=True, message_id=message.message_id)
        return True