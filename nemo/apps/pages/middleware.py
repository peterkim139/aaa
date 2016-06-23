import datetime
from django.core.cache import cache
from django.conf import settings


class ActiveUserMiddleware:

    @staticmethod
    def process_request(request):
        current_user = request.user
        if request.user.is_authenticated():
            now = datetime.datetime.now()
            cache.set('seen_%s' % (current_user.email), now,
                      settings.USER_LASTSEEN_TIMEOUT)
