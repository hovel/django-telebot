from django.apps import AppConfig

class BaseConfig(AppConfig):
    name = 'telebot.base'
    verbose_name = 'Bot basic functions'

class LoggerConfig(AppCOnfig):
    name = 'telebot.logger'
    verbose_name = 'Log everything to database functionality'