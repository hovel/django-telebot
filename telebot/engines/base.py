import importlib
import logging
from uuid import uuid4
from functools import singledispatchmethod
from abc import ABC, abstractmethod
from django.contrib.auth.models import User
from django.conf import settings
from telebot.base.models import UserLink, Bot
from telebot.helpers import log_system_event, log_message
from telebot.logger import FROM_USER

logger = logging.getLogger('telebot.engine')

USER_REGISTER_CALLBACK = getattr(settings, 'USER_REGISTER_CALLBACK', None)
TELEBOT_REGISTER_ON_INCOMING = getattr(settings, 'TELEBOT_REGISTER_ON_INCOMING', True)

if type(USER_REGISTER_CALLBACK) == str:
    USER_REGISTER_CALLBACK = importlib.import_module(USER_REGISTER_CALLBACK)


class AbstractEngine(ABC):
    '''
    Abstract bot with at least
    basic functions:
    - __init__
    - _send_message
    '''
    @abstractmethod
    def __init__(self, bot: Bot):
        self.bot_obj = bot
        self.register_on_send = True
        self.relink_by_chat_id = True

    @abstractmethod
    def _send_message(self, link, text: str, **kwargs) -> bool:
        pass

    def send_message(self, user=None, text: str='', chat_id=None, **kwargs) -> bool:
        if (not user) and (not chat_id):
            raise AttributeError('Either user or chat_id should be provided for "send_message"')
        if chat_id:
            link = UserLink.objects.filter(chat_id=chat_id, bot=self.bot_obj).first()
        elif type(user)==str:
            link = UserLink.objects.filter(chat_id=user, bot=self.bot_obj).first()
            chat_id = user
        elif type(user)==int:
            link = UserLink.objects.filter(chat_id=user, bot=self.bot_obj).first()
            chat_id = str(user)
        elif type(user)==User:
            link = UserLink.objects.filter(user=user, bot=self.bot_obj).first()
        elif type(user)==UserLink:
            link = user
        else:
            raise NotImplementedError(f'Can not send message to unknown user type, \
             can send only to: chat_id, django.contrib.auth.models.User or telebot.base.modes.UserLink, \
                 got {type(user)} type')
        if (not link) and (self.register_on_send) and (chat_id):
            link = self.register_user(chat_id)
        if not link:
            raise ValueError(f'Trying to send to user {user} but can\'t get chat_id')
        self._send_message(link, text, **kwargs)

    def register_user(self, chat_id: str) -> UserLink:
        link = UserLink.objects.filter(bot=self.bot_obj, chat_id=chat_id).first()
        if link:
            logger.warning(f'Link for bot: {self.bot_obj.id} and chat_id: {chat_id} already established for user: {link.user.id}')
            return link
        u_name = chat_id
        user = User.objects.filter(username=chat_id).first()
        if user and (not self.relink_by_chat_id):
            # User with username chat_id already exist
            # Create new user with uuid4 username
            logger.warning(f'User with username {u_name} like chat_id already exists. Creating new with uuid4 username')
            u_name = uuid4()
        if not user:
            user = User.objects.create_user(username=u_name)
        link = UserLink.objects.create(user=user, bot=self.bot_obj, chat_id=chat_id)
        if USER_REGISTER_CALLBACK:
           USER_REGISTER_CALLBACK(self, chat_id)
        return link

    def log_incoming(self, chat_id, message: str, addional_info: str='') -> None:
        link = UserLink.objects.filter(bot=self.bot_obj, chat_id=chat_id).first()
        if not link:
            if TELEBOT_REGISTER_ON_INCOMING:
                link = self.register_user(chat_id)
            else:
                raise ValueError(f'Link for chat_id {chat_id} and bot {self.bot_obj.id} was not found')
        log_message(link, message, FROM_USER, success=True, addional_info=addional_info)
