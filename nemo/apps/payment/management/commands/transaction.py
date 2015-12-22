from django.core.management.base import BaseCommand
import datetime
import logging
import braintree
import os
from django.db import transaction
from django.utils import timezone
from payment.models import Rent
from payment.utils import payment_connection,error_logging

class Command(BaseCommand):

    def handle(self, *args, **options):
        payment_connection()
        today = timezone.now() - datetime.timedelta(days=1)
        rents = Rent.objects.filter(status='approved',rent_date__lte=today)
        for rent in rents:
            result = braintree.Transaction.release_from_escrow(rent.transaction)
            if result.is_success:
                Rent.objects.filter(id=rent.id).update(status='paid',transaction_status='settled')
            else:
                for error in result.errors.deep_errors:
                    text = str(rent.id) + '-' + error.message
                    error_logging(text)
                Rent.objects.filter(id=rent.id).update(transaction_status='error')