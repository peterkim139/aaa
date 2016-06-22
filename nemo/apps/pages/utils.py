from decimal import Decimal
from django.conf import settings
import uuid


def save_file(request, uploaded, filename, path, raw_data=True):

    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    request.session['image_filename'] = filename
    try:
        fd = open('%s/%s' % (settings.MEDIA_ROOT, str(path) + str(filename)), 'wb')
        if raw_data:
            foo = uploaded.read( 1024 )
            while foo:
                fd.write( foo )
                foo = uploaded.read( 1024 )
        return filename
    except IOError:
        return False

#################################  json serialize datetime ###################


def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj


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
