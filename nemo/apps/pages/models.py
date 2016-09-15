from django.db import models
import datetime
from django.core.cache import cache
from django.conf import settings
from accounts.models import User
from category.models import Params
from accounts.mixins import AbstractDateTime


class Image(AbstractDateTime):

    param_image = models.ForeignKey(Params)
    image_name = models.CharField(max_length=255, blank=False, default='')

    class Meta:
        ordering = ["id"]
        db_table = "images"
        get_latest_by = "created"


class Thread(AbstractDateTime):
    last_message = models.TextField(max_length=500)
    user1_id = models.IntegerField()
    user2_id = models.IntegerField()
    item_id = models.IntegerField(blank=False, default=1)

    @staticmethod
    def last_seen(email):
        return cache.get('seen_%s' % email)

    def online(self, email):
        if self.last_seen(email):
            now = datetime.datetime.now()
            if now > self.last_seen(email) + datetime.timedelta(
                         seconds=settings.USER_ONLINE_TIMEOUT):
                return False
            else:
                return True
        else:
            return False

    class Meta:
        db_table = 'thread'


class Message(AbstractDateTime):
    thread = models.ForeignKey(Thread)
    unread = models.IntegerField()
    message = models.TextField(max_length=500)
    from_user_id = models.ForeignKey(User, related_name="from_user_id")
    to_user_id = models.ForeignKey(User, related_name="to_user_id")

    class Meta:
        db_table = 'message'
