import datetime
from Crypto.Cipher import AES
import base64
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
from category.models import Params
from accounts.mixins import LoginRequiredMixin
from payment.generate import NemoEncrypt



class RequestsView(LoginRequiredMixin,TemplateView, View):
    template_name = 'pages/requests.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(RentView, self).get_context_data(**kwargs)
#         context['form'] = RentForm()
#         if 'form' in kwargs:
#             context.update({'form': RentForm(data=self.request.POST)})
#         return context
#
#     def get(self, request,id):
#
#         return self.render_to_response(self.get_context_data())
#
#     def post(self, request,id):
#
#         form = RentForm(data=request.POST)
#         if form.is_valid():
#             expiration_date = form.cleaned_data['month'] +'/' + form.cleaned_data['year']
#             braintree.Configuration.configure(braintree.Environment.Sandbox,
#                               merchant_id="5d5xq56qq88nnnv3",
#                               public_key="xsp7n87828mv5j9f",
#                               private_key="407840324125e98f5efc1d4666101ed5")
#
#             customer = braintree.Customer.create({
#                 "first_name": request.user.first_name,
#                 "last_name": request.user.last_name,
#                 "email": request.user.email,
#                 "credit_card": {
#                 "number": form.cleaned_data['card_number'],
#                 "expiration_date": expiration_date,
#                 "cvv": form.cleaned_data['cvv']
#                 }
#             })
#             if customer.is_success:
#                 encrypt= NemoEncrypt()
#                 customer_id = encrypt.encrypt_val(customer.customer.id)
#                 item = Params.objects.get(id=id)
#                 User.objects.filter(id=request.user.id).update(customer_id=customer_id)
#                 rent = Rent()
#                 rent.status = 'pending'
#                 rent.price = item.price
#                 rent.rent_date = form.cleaned_data['rent_date']
#                 rent.param_id = item.id
#                 rent.user_id = request.user.id
#                 rent.save()
#             messages.success(request, "Your request has been sent successfully")
#             return HttpResponseRedirect('/')
#
#         else:
#             return self.render_to_response(self.get_context_data(form=form))