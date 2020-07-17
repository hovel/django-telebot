# Profile

from django.contrib.auth.models import User
from django.db import models
from . import ENGINES_LIST, ENGINES, load_engines

ENGINES_NAMES = []
for name in ENGINES_LIST:
    ENGINES_NAMES.append((name, name))


class Bot(models.Model):
    name = models.CharField(max_length=50, unique=True)
    engine = models.CharField(max_length=20, choices=ENGINES_NAMES)
    token = models.CharField(max_length=200, null=True, blank=True)

    def get_engine(self):
        if not ENGINES:
            load_engines()
        return ENGINES[self.engine].Engine(self)


class UserLink(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE)
    chat_id = models.CharField(max_length=100, db_index=True)
    active = models.BooleanField(default=True)

    class Meta:
        unique_together=[['bot', 'chat_id']]
