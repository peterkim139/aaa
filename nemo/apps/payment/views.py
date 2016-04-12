import datetime
import braintree
from Crypto.Cipher import AES
import base64
from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.http import HttpResponseRedirect, HttpResponse
from  django.template.context_processors import csrf
from django.contrib import messages
from django.shortcuts import redirect
from .forms import ConnectForm,RentForm
from accounts.mixins import LoginRequiredMixin
from payment.generate import NemoEncrypt
from django.core import serializers
from django.conf import settings
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from .models import User,Params,Rent
from payment.utils import payment_connection,new_rent_mail

class ConnectView(LoginRequiredMixin,TemplateView, View):
    template_name = 'payment/connect.html'

    def get_context_data(self, **kwargs):
        context = super(ConnectView, self).get_context_data(**kwargs)
        context['form'] = ConnectForm()
        if 'form' in kwargs:
            context.update({'form': ConnectForm(data=self.request.POST)})
        return context

    def get(self, request):

        return self.render_to_response(self.get_context_data())

    def post(self, request):
        form = ConnectForm(data=request.POST)
        if form.is_valid():
            payment_connection()
            year = request.POST['birthdate_year']
            month = request.POST['birthdate_month']
            day = request.POST['birthdate_day']
            date_of_birth = year+'-'+month+'-'+day
            merchant_account_params = {
            'individual': {
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
                'phone': form.cleaned_data['phone_number'],
                'date_of_birth': date_of_birth,
                'address': {
                    'street_address': form.cleaned_data['street_address'],
                    'locality': form.cleaned_data['locality'],
                    'region': form.cleaned_data['region'],
                    'postal_code': form.cleaned_data['postal_code']
                }
            },
            'funding': {
                'destination': braintree.MerchantAccount.FundingDestination.Bank,
                'account_number': form.cleaned_data['account_number'],
                'routing_number': form.cleaned_data['routing_number'],
            },
            "tos_accepted": True,
            "master_merchant_account_id": "sipan",
            }
            result = braintree.MerchantAccount.create(merchant_account_params)
            if result.is_success:
                try:
                    User.objects.filter(id=request.user.id).update(merchant_id=result.merchant_account.id)
                    messages.success(request, "Your account has been created successfully")
                    return HttpResponseRedirect('/list')
                except Exception as e:
                    messages.error(request, "Error")
                    return HttpResponseRedirect('/list')
            else:
                for error in result.errors.deep_errors:
                    error_message = error.message

                messages.error(request, error_message)
                return self.render_to_response(self.get_context_data(form=form))
        else:
            return self.render_to_response(self.get_context_data(form=form))



class RentView(LoginRequiredMixin,TemplateView, View):
    template_name = 'payment/rent.html'
    id = ''
    def get_context_data(self, **kwargs):
        context = super(RentView, self).get_context_data(**kwargs)
        context['form'] = RentForm()
        blockdays = Rent.objects.filter(Q(status='pending',param_id=self.id) | Q(status='approved',param_id=self.id))
        dates = {}
        for blockday in blockdays:
            dates[ blockday.rent_date.strftime('%Y-%m-%d')] = blockday.start_date.strftime('%Y-%m-%d')
        context['blockdays'] = dates
        if 'form' in kwargs:
            context.update({'form': RentForm(data=self.request.POST)})
        return context

    def get(self, request,id):
        self.id = id
        return self.render_to_response(self.get_context_data())

    def post(self, request,id):

        self.id = id
        form = RentForm(data=request.POST)
        if form.is_valid():

            blockdays = Rent.objects.filter(Q(status='pending',param_id=self.id) | Q(status='approved',param_id=self.id))
            dates = []
            for blockday in blockdays:
                while blockday.start_date <= blockday.rent_date:
                    dates.append(blockday.start_date.strftime('%Y-%m-%d'))
                    blockday.start_date = blockday.start_date + datetime.timedelta(days=1)

            rent_date = datetime.datetime.strptime(form.cleaned_data['rent_date'], '%Y-%m-%d')
            start_date = datetime.datetime.strptime(form.cleaned_data['start_date'], '%Y-%m-%d')
            while start_date <= rent_date:
                if start_date.strftime('%Y-%m-%d') in dates:
                    messages.error(request, "Invalid Date Range")
                    return HttpResponseRedirect('/payment/rent/'+id)
                start_date = start_date + datetime.timedelta(days=1)

            encrypt= NemoEncrypt()
            current_user = User.objects.get(id=request.user.id)
            expiration_date = form.cleaned_data['month'] +'/' + form.cleaned_data['year']
            payment_connection()
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
                customer_id = encrypt.encrypt_val(customer.customer.id)
                item = Params.objects.get(id=id)
                User.objects.filter(id=request.user.id).update(customer_id=customer_id)
                rent = Rent()
                rent.status = 'pending'
                rent.price = item.price
                rent.start_date = form.cleaned_data['start_date']
                rent.rent_date = form.cleaned_data['rent_date']
                rent.owner_id = item.item_owner_id
                rent.param_id = item.id
                rent.user_id = request.user.id
                rent.save()
                seller = User.objects.get(id=item.item_owner_id)
                new_rent_mail(request,seller.email,request.user.first_name,item.name,seller.first_name,rent.id)
            messages.success(request, "Your request has been sent successfully")
            return HttpResponseRedirect('/')

        else:
            return self.render_to_response(self.get_context_data(form=form))