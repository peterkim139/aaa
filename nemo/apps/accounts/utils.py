
import hashlib
import random

from django.core.mail import EmailMessage
from django.template import Context
from django.template import loader
from django.conf import settings


def generate_activation_key(email):
    salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
    if isinstance(email, unicode):
        email = email.encode('utf-8')
    activation_key = hashlib.sha1(salt + email).hexdigest()
    return activation_key


def reset_mail(request, email, first_name, reset_key):
    subject = 'Reset account password'
    from_email = settings.AUTO_REPLY
    to = [email]
    context = Context({
        'username': first_name,
        'reset_key': reset_key,
        'site_name': settings.ADMIN_EMAIL,
        'absolute_url': request.META['HTTP_HOST']
    })
    content = loader.render_to_string('accounts/emails/password_reset_email.html', context)
    msg = EmailMessage(subject, content, from_email, to=to).send()

