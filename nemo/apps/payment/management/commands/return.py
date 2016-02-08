from django.core.management.base import BaseCommand
import datetime
import braintree
from django.utils import timezone
from payment.models import Rent
from accounts.models import User
from payment.utils import return_rent_client
from django.db.models import Q

class Command(BaseCommand):

    def handle(self, *args, **options):
        today = timezone.now() + datetime.timedelta(days=1)
        rents = Rent.objects.filter(start_date__lte=today,status='approved')
        if rents:
            for rent in rents:
                info = Rent.objects.get(id=rent.id)
                return_rent_client(info)