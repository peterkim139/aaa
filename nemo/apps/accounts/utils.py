
import hashlib
import random
import mandrill
from django.template import Context
from django.template import loader
from django.conf import settings
from django.contrib.gis.geoip import GeoIP


mandrill_client = mandrill.Mandrill(settings.MANDRILL_KEY)

def generate_activation_key(email):
    salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
    if isinstance(email, unicode):
        email = email.encode('utf-8')
    activation_key = hashlib.sha1(salt + email).hexdigest()
    return activation_key


def reset_mail(request, email, first_name, reset_key):

    mandrill_client = mandrill.Mandrill(settings.MANDRILL_KEY)

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
    message = {
        'subject' : 'Reset account password',
        'bcc_address': 'message.bcc_address@example.com',
        'from_email': 'message.from_email@example.com',
        'from_name': 'NEMO',
        'html':content,
        'to': [{'email': email,
             'name': first_name,
             'type': 'to'}],
        'return_path_domain': 'nemo.codebnb.me',
        'signing_domain': 'nemo.codebnb.me',
        'tracking_domain': 'nemo.codebnb.me',
    }
    result = mandrill_client.messages.send(message=message, async=False, ip_pool='', send_at='')

def confirm_register_mail(request, email, first_name, last_name, zip_code):

    mandrill_client = mandrill.Mandrill(settings.MANDRILL_KEY)

    subject = 'Thanks for registering'
    from_email = settings.AUTO_REPLY
    to = [email]
    context = Context({
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'zip_code': zip_code,
        'site_name': settings.ADMIN_EMAIL,
        'absolute_url': request.META['HTTP_HOST']
    })
    content = loader.render_to_string('accounts/emails/confirm_register_email.html', context)
    message = {
        'subject' : subject,
        'bcc_address': 'message.bcc_address@example.com',
        'from_email': 'message.from_email@example.com',
        'from_name': 'NEMO',
        'html':content,
        'to': [{'email': email,
             'name': first_name,
             'type': 'to'}],
        'return_path_domain': 'nemo.codebnb.me',
        'signing_domain': 'nemo.codebnb.me',
        'tracking_domain': 'nemo.codebnb.me',
    }
    result = mandrill_client.messages.send(message=message, async=False, ip_pool='', send_at='')

def get_coordinates(request):

    g = GeoIP()
    x_forwarded_for = request.META.get('HTTP_CLIENT_IP')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    lat_lng = g.lat_lon(ip)

    cookies = request.COOKIES.get('lat_lng')
    if cookies:
        cookies = request.COOKIES.get('lat_lng').split(',')
    if cookies and cookies[0] and cookies[1]:
        latitude = cookies[0]
        longitude = cookies[1]
    elif lat_lng:
        latitude = lat_lng[0]
        longitude = lat_lng[1]
    else:
        latitude = 42.396645
        longitude = -71.109388

    coordinates = [latitude,longitude]
    return coordinates

