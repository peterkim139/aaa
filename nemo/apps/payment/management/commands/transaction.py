from django.core.management.base import BaseCommand
import datetime
import braintree
from django.utils import timezone
from payment.models import Rent
from payment.utils import payment_connection, error_logging, seller_transaction_email
from payment.emails import seller_transaction_email


class Command(BaseCommand):

    def handle(self, *args, **options):
        payment_connection()
        today = timezone.now() - datetime.timedelta(days=1)
        rents = Rent.objects.filter(status='approved', rent_date__lte=today)
        if rents:
            for rent in rents:
                result = braintree.Transaction.release_from_escrow(rent.transaction)
                if result.is_success:
                    seller_transaction_email(rent)
                    Rent.objects.filter(id=rent.id).update(status='paid', transaction_status='settled')
                else:
                    for error in result.errors.deep_errors:
                        rent_date = rent.rent_date.strftime('%Y-%m-%d')
                        rent_date = ' Rent has been finished- '+str(rent_date)
                        text = error.message+' Rent id is '+str(rent.id)+'.'+rent_date
                        error_logging(text)
                    Rent.objects.filter(id=rent.id).update(transaction_status='error')
