from django.core.management.base import BaseCommand
import datetime
import os
from django.db import transaction
from django.utils import timezone
from payment.models import Rent


class Command(BaseCommand):

    def handle(self, *args, **options):
        today = timezone.now() - datetime.timedelta(days=1)
        rents = Rent.objects.filter(status='approved',rent_date__lte=today)
        for rent in rents:
            print rent.id