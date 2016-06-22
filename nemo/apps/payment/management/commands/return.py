from django.core.management.base import BaseCommand
import datetime
from django.utils import timezone
from payment.models import Rent
from payment.emails import return_rent_client


class Command(BaseCommand):

    def handle(self, *args, **options):
        today = timezone.now() + datetime.timedelta(days=1)
        rents = Rent.objects.filter(start_date__lte=today, status='approved')
        if rents:
            for rent in rents:
                info = Rent.objects.get(id=rent.id)
                return_rent_client(info)
