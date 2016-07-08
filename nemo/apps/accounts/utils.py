import hashlib
import os
from django.contrib.gis.geoip import GeoIP


def generate_activation_key(email):
    salt = os.urandom(10).encode('hex')
    if isinstance(email, unicode):
        email = email.encode('utf-8')
    activation_key = hashlib.sha1(salt + email).hexdigest()
    return activation_key


def get_coordinates(request):

    lat_lng = ''
    cookies = request.COOKIES.get('lat_lng')
    if cookies:
        if 'expires' in cookies:
            cookies = cookies.split("expires",1)[0]
        cookies = cookies.split(',')
        try:
            float(cookies[0])
            float(cookies[1])
        except ValueError:
            cookies = ''
    else:
        g = GeoIP()
        x_forwarded_for = request.META.get('HTTP_CLIENT_IP')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        lat_lng = g.lat_lon(ip)
        
    if cookies and cookies[0] and cookies[1]:
        latitude = cookies[0]
        longitude = cookies[1]
    elif lat_lng:
        latitude = lat_lng[0]
        longitude = lat_lng[1]
    else:
        latitude = 42.396645
        longitude = -71.109388

    coordinates = [latitude, longitude]
    return coordinates

