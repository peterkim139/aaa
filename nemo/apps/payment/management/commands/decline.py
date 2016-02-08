from django.core.management.base import BaseCommand
import datetime
import braintree
from django.utils import timezone
from payment.models import Rent
from accounts.models import User
from payment.utils import payment_connection,error_logging,expired_rent_seller,expired_rent_client
from django.db.models import Q

class Command(BaseCommand):

    def handle(self, *args, **options):
        today = timezone.now() - datetime.timedelta(days=2)
        rents = Rent.objects.filter(Q(status='pending',created__lte=today) | Q(status='pending',rent_date__lte=today))
        if rents:
            for rent in rents:
                Rent.objects.filter(id=rent.id).update(status='expired')
                info = Rent.objects.get(id=rent.id)
                expired_rent_seller(info)
                expired_rent_client(info)