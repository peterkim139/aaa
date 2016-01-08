import datetime
import braintree
from decimal import Decimal
from Crypto.Cipher import AES
import base64
from django.utils import timezone
from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.http import HttpResponseRedirect, HttpResponse
from  django.template.context_processors import csrf
from django.contrib import messages
from django.shortcuts import redirect
from django.core import serializers
from django.conf import settings
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from payment.models import Rent
from .forms import RentForm
from accounts.models import User
from accounts.mixins import LoginRequiredMixin
from payment.generate import NemoEncrypt
from payment.utils import payment_connection


class RequestsView(LoginRequiredMixin,TemplateView, View):
    template_name = 'pages/requests.html'


    def get(self,request):

        requests = Rent.objects.filter(owner_id=request.user.id)

        return self.render_to_response({'requests':requests})

class RequestView(LoginRequiredMixin,TemplateView, View):
    template_name = 'pages/request.html'
    id = 0
    def get_context_data(self, **kwargs):

            context = super(RequestView, self).get_context_data(**kwargs)
            context['form'] = RentForm()
            requests = Rent.objects.get(param_id=self.id)
            context.update({'requests': requests})
            if 'form' in kwargs:
                context.update({'form': RentForm(self.request.POST)})

            return context

    def get(self,request,id):
        self.id = id
        return self.render_to_response(self.get_context_data())

    def post(self,request,id):
        self.id = id
        if request.POST['rent']:
            payment_connection()
            rent = int(request.POST['rent'])
            print rent
            if request.POST['action'] == 'Approve':
                status = 'approved'
            elif request.POST['action'] == 'Decline':
                status = 'seller_declined'
            else:
                status = 'seller_canceled'

            requests = Rent.objects.get(owner_id=request.user.id,id=rent)
            if requests.status == 'pending' or requests.status == 'approved':
                encrypt= NemoEncrypt()
                current_user = User.objects.get(id=requests.owner_id)
                orderer = User.objects.get(id=requests.user_id)
                if status == 'approved':
                    customer_id = encrypt.decrypt_val(orderer.customer_id)
                    TWOPLACES = Decimal(10) ** -2
                    fee = Decimal(requests.price*5/100).quantize(TWOPLACES)
                    result = braintree.Transaction.sale({
                        "amount": requests.price,
                        "merchant_account_id": current_user.merchant_id,
                        "customer_id": customer_id,
                        "options": {
                        "submit_for_settlement": True,
                        "hold_in_escrow": True,
                        },
                        "service_fee_amount": fee
                    })
                    if result.is_success:
                        transaction = result.transaction
                        Rent.objects.filter(owner_id=request.user.id,id=rent).update(transaction=transaction.id,status=status,modified=timezone.now())
                        messages.success(request, "The request has been approved")
                    else:
                        messages.error(request, "There are some errors in transaction process")

                elif status == 'seller_declined':
                    Rent.objects.filter(owner_id=request.user.id,id=rent).update(status=status)
                    messages.success(request, "Request has been declined")

                elif status == 'seller_canceled':
                    form = RentForm(data=request.POST)
                    if form.is_valid():
                        expiration_date = form.cleaned_data['month'] +'/' + form.cleaned_data['year']
                        if current_user.customer_id:
                            customer = braintree.Customer.update(encrypt.decrypt_val(current_user.customer_id), {
                                "credit_card": {
                                    "number": form.cleaned_data['card_number'],
                                    "expiration_date": expiration_date,
                                    "cvv": form.cleaned_data['cvv']
                                }
                            })
                        else:
                            customer = braintree.Customer.create({
                                "first_name": request.user.first_name,
                                "last_name": request.user.last_name,
                                "email": request.user.email,
                                "credit_card": {
                                "number": form.cleaned_data['card_number'],
                                "expiration_date": expiration_date,
                                "cvv": form.cleaned_data['cvv']
                                }
                            })
                            if customer.is_success:
                                User.objects.filter(id=request.user.id).update(customer_id=encrypt.encrypt_val(customer.customer.id))
                                current_user = User.objects.get(id=requests.owner_id)
                        today = timezone.now() + datetime.timedelta(days=1)
                        customer_id = encrypt.decrypt_val(current_user.customer_id)
                        if today < requests.rent_date:
                            amount = '2.00'
                        else:
                            amount  = '5.00'

                        transaction = braintree.Transaction.find(requests.transaction)
                        if transaction.escrow_status == 'held':
                            refund = braintree.Transaction.refund(requests.transaction)
                        elif transaction.escrow_status == 'hold_pending':
                            refund = braintree.Transaction.void(requests.transaction)

                        if refund.is_success:
                            result = braintree.Transaction.sale({
                                "amount": amount,
                                "customer_id": customer_id,
                                "options": {
                                    "submit_for_settlement": True
                                }
                            })
                            if result.is_success:
                                messages.success(request, "Request has been canceled")
                            else:
                                messages.error(request, "There is an error in refund process")

                        Rent.objects.filter(owner_id=request.user.id,id=rent).update(status=status)
                    else:
                        return self.render_to_response(self.get_context_data(form=form))
            else:
                messages.error(request, "There is no request")
        else:
            messages.error(request, "There is no request")

        return HttpResponseRedirect('/profile/request/'+id)
        return self.render_to_response({'requests':requests})


class MyRequestsView(LoginRequiredMixin,TemplateView, View):
    template_name = 'pages/my_requests.html'
    def get(self,request,id=None):
        cancel = 0
        if id:
            self.template_name = 'pages/my_request.html'
            requests = Rent.objects.get(param_id=id)
            hour = timezone.now() - datetime.timedelta(hours=2)
            if requests.modified < hour:
                cancel = 1
        else:
            requests = Rent.objects.filter(user_id=request.user.id)

        return self.render_to_response({'requests':requests,'cancel':cancel})

    def post(self,request,id):

        if request.POST['rent']:
            payment_connection()
            rent = int(request.POST['rent'])
            if request.POST['action'] == 'Decline':
                status = 'customer_declined'
            else:
                status = 'customer_canceled'

            requests = Rent.objects.get(user_id=request.user.id,id=rent)
            if requests.status == 'pending' or requests.status == 'approved':
                encrypt= NemoEncrypt()
                current_user = User.objects.get(id=requests.owner_id)
                orderer = User.objects.get(id=requests.user_id)
                if requests.status == 'customer_declined':
                    Rent.objects.filter(user_id=request.user.id,id=rent).update(status=status)
                    messages.success(request, "Request has been declined")
                else:
                    today = timezone.now() + datetime.timedelta(days=1)
                    customer_id = encrypt.decrypt_val(current_user.customer_id)
                    amount = requests.price*50/100
                    if today >= requests.rent_date:
                        result = braintree.Transaction.refund(requests.transaction,amount)
                        if result.is_success:
                            Rent.objects.filter(user_id=request.user.id,id=rent).update(status=status)
                            messages.success(request, "Request has been canceled")
                        else:
                            messages.error(request, "There is an error in refund process")
            else:
                messages.error(request, "There is no request")
        else:
            messages.error(request, "There is no request")
        return HttpResponseRedirect('/profile/my_requests/'+id)