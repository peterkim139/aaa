from decimal import Decimal
from django.conf import settings
import uuid
import datetime
import pytz
from django.utils import timezone



def save_file(request, uploaded, filename, path, raw_data=True):

    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    request.session['image_filename'] = filename
    try:
        fd = open('%s/%s' % (settings.MEDIA_ROOT, str(path) + str(filename)), 'wb')
        if raw_data:
            foo = uploaded.read(1024)
            while foo:
                fd.write(foo)
                foo = uploaded.read(1024)
        return filename
    except IOError:
        return False

#  json serialize datetime ###################


def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj


def handel_datetime(request):
    tz_number = request.COOKIES.get('timezone')
    if 'expires' in tz_number:
            tz_number = int(tz_number.split("expires",1)[0])
    hours = -4
    if type(tz_number) is int:
        hours = tz_number

    utc_offset = datetime.timedelta(hours=hours, minutes=0)
    now = datetime.datetime.now(pytz.utc)
    for tz in map(pytz.timezone, pytz.all_timezones_set):
        if now.astimezone(tz).utcoffset() == utc_offset:
            tz_name = tz.zone
    timezone.activate(pytz.timezone(tz_name))

def refund_price(price):

    twoplaces = Decimal(10) ** -2
    list = {}
    if price > 20:
        amount = Decimal(price*100-970)/Decimal(97.1)
        list['amount'] = amount.quantize(twoplaces)
        list['credit'] = Decimal(price*50/100).quantize(twoplaces)
    else:
        amount = Decimal(price*50+30)/Decimal(97.1)
        list['amount'] = amount.quantize(twoplaces)
        list['credit'] = Decimal(price*25/100).quantize(twoplaces)

    return list
