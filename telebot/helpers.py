from telebot.logger.models import MessageLogRecord, SystemLogRecord
from datetime import datetime
from django.conf import settings
from telebot.logger import LOG_LEVEL_ALL, LOG_LEVEL_ERRORS, LOG_LEVEL_NONE, AVAILABLE_LOG_LEVELS, FROM_BOT, FROM_USER


LOG_LEVEL = getattr(settings, 'TELEBOT_LOG_LEVEL', LOG_LEVEL_ALL)

if LOG_LEVEL not in AVAILABLE_LOG_LEVELS:
    raise ValueError(f'TELEBOT_LOG_LEVEL should be one of: {AVAILABLE_LOG_LEVELS}')

def log_message(user_link, message, direction, success, error=None, message_id=None, addional_info=None):
    if LOG_LEVEL == LOG_LEVEL_NONE:
        return
    if (LOG_LEVEL == LOG_LEVEL_ERRORS) and (not error):
        return
    MessageLogRecord.objects.create(
        link=user_link, message=message,
        direction=direction, success=success,
        error=error, date=datetime.now()
        )
    return

def log_system_event(event_class, event, user_link=None):
    SystemLogRecord.objects.create(link=user_link, event=event, event_class=event_class)
    return 