import importlib
from django.conf import settings

default_app_config = 'telebot.apps.BaseConfig'

ENGINES_LIST = getattr(settings, 'TELEBOT_ENGINES', {'telegram': 'telebot.engines.telegram'})
ENGINES = {}

def load_engines():
    for name, engine_lib in ENGINES_LIST.items():
        ENGINES[name] = importlib.import_module(engine_lib)