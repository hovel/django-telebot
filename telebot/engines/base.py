import importlib
import logging
from uuid import uuid4
from functools import singledispatchmethod
from abc import ABC, abstractmethod
from django.contrib.auth.models import User
from django.conf import settings
from telebot.base.models import UserLink, Bot
from telebot.helpers import log_system_event

logger = logging.getLogger('telebot.engine')

USER_REGISTER_CALLBACK = getattr(settings, 'USER_REGISTER_CALLBACK', None)

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

    @abstractmethod
    def _send_message(self, link, message: str, kwgs: dict=None) -> bool:
        pass

    @singledispatchmethod
    def send_message(self, user, message: str, kwgs: dict=None) -> bool:
        raise NotImplementedError('Can not send message to unknown user type, \
             can send only to: chat_id, django.contrib.auth.models.User or telebot.base.modes.UserLink')

    @send_message.register
    def _(self, user: int, message: str, kwgs: dict=None) -> bool:
        # Send message using user chat_id
        link = UserLink.objects.filter(chat_id=user).first()
        if not link:
           raise ValueError(f'UserLink with chat_id {user} was not found')
        return self.send_message(link, message, kwgs)
      
    @send_message.register
    def _(self, user: User, message: str, kwgs: dict=None) -> bool:
        link = UserLink.objects.filter(user=user).first()
        if not link:
           raise ValueError(f'UserLink with chat_id {user} was not found')
        return self.send_message(link, message, kwgs)
    
    @send_message.register
    def _(self, user: UserLink, message: str, kwgs: dict=None) -> bool:
        if kwgs and type(kwgs)!=dict:
            raise TypeError('Keyword arguments for send message should be dictionary')
        kwargs = kwgs or {}
        self._send_message(user, message, kwgs)

    def register_user(self, chat_id: str) -> UserLink:
        link = UserLink.objects.filter(bot=self.bot_obj, chat_id=chat_id).first()
        if link:
            logger.warning(f'Link for bot: {self.bot_obj.id} and chat_id: {chat_id} already established for user: {link.user.id}')
            return link
        u_name = chat_id
        user = User.objects.filter(username=chat_id).first()
        if user:
            # User with username chat_id already exist
            # Create new user with uuid4 username
            logger.warning(f'User with username {u_name} like chat_id already exists. Creating new with uuid4 username')
            u_name = uuid4()
        user = User.objects.create_user(username=u_name)
        link = UserLink.objects.create(user=user, bot=self.bot_obj, chat_id=chat_id)
        if USER_REGISTER_CALLBACK:
           USER_REGISTER_CALLBACK(self, chat_id)