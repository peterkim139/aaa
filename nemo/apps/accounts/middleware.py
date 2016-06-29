from social.apps.django_app.middleware import SocialAuthExceptionMiddleware
from django.http import HttpResponseRedirect
from social.exceptions import AuthCanceled

class SocialAuthExceptionMiddleware(SocialAuthExceptionMiddleware):

    @staticmethod
    def process_exception(request, exception):

        if type(exception) == AuthCanceled:
            response = HttpResponseRedirect('/')
            response.set_cookie('exist', 'cancel_error')
            return response
