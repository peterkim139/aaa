import braintree
from django.contrib import admin
from .models import Rent, User
from payment.utils import payment_connection
from payment.emails import admin_cancel_rent_to_client, admin_cancel_rent_to_seller


def refund_transaction(modeladmin, request, queryset):

    for item in queryset:
        item = Rent.objects.get(id=item.id)
        if item.transaction and item.status == 'approved':
            payment_connection()
            refund = braintree.Transaction.refund(item.transaction)
            if refund.is_success:
                Rent.objects.filter(id=item.id).update(status='admin_canceled')
                admin_cancel_rent_to_client(item)
                admin_cancel_rent_to_seller(item)


class RentAdmin(admin.ModelAdmin):
    model = Rent
    list_display = ['id', 'client', 'seller', 'item', 'price', 'status', 'rent_date']

    @staticmethod
    def client(obj):
        return obj.user.first_name + ' ' + obj.user.last_name

    @staticmethod
    def seller(obj):
        return obj.owner.first_name + ' ' + obj.owner.last_name

    @staticmethod
    def item(obj):
        return obj.param.name

    @staticmethod
    def price(obj):
        return obj.price

    @staticmethod
    def rent_date(obj):
        return obj.rent_date

    readonly_fields = ['created', 'modified']
    search_fields = ['id']
    actions = [refund_transaction]

admin.site.register(Rent, RentAdmin)
