from django.core.management.base import BaseCommand

import os
from django.db import transaction


class Command(BaseCommand):

    def handle(self, *args, **options):
            print 'sss'