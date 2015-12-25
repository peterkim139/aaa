import datetime
import json
import logging
from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.contrib.auth import login,logout
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from  django.template.context_processors import csrf
from django.contrib import messages
from django.shortcuts import redirect
from django.core import serializers
from django.contrib.auth.hashers import make_password
from .forms import RegistrationForm,AuthenticationForm,ResetForm,ChangePasswordForm,SocialForm
from accounts.mixins import LoginRequiredMixin
from accounts.utils import generate_activation_key,reset_mail
from django.conf import settings
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from accounts.models import User
import braintree

class HomeView(TemplateView):
    template_name = 'accounts/home.html'
    # def get(self, request):
    #
    #     braintree.Configuration.configure(braintree.Environment.Sandbox,
    #                               merchant_id="5d5xq56qq88nnnv3",
    #                               public_key="xsp7n87828mv5j9f",
    #                               private_key="407840324125e98f5efc1d4666101ed5")

        # result = braintree.Customer.create({
        #     "first_name": "firstname",
        #     "last_name": "lastname",
        #     "email": "test@example.com",
        #     "credit_card": {
        #     "number": "4111111111111111",
        #     "expiration_date": "05/2016",
        #     "cvv": "100"
        #     }
        # })
        # print result.customer.id

        # result = braintree.Transaction.sale({
        #     "amount": "100.00",
        #     "merchant_account_id": "sipan_margaryan_instant_3srs62xn",
        #     "customer_id": "82545187",
        #     "options": {
        #     "submit_for_settlement": True,
        #     "hold_in_escrow": True,
        #     },
        #     "service_fee_amount": "10.00"
        # })
        # if result.is_success:
        #     print result.transaction.id
        # merchant_account_params = {
        # 'individual': {
        #     'first_name': "Jane",
        #     'last_name': "Doe",
        #     'email': "jane@14ladders.com",
        #     'phone': "5553334444",
        #     'date_of_birth': "1981-11-19",
        #     'ssn': "456-45-4567",
        #     'address': {
        #         'street_address': "111 Main St",
        #         'locality': "Chicago",
        #         'region': "IL",
        #         'postal_code': "60622"
        #     }
        # },
        # "tos_accepted": True,
        # "master_merchant_account_id": "w77h5ppxjvdzsqfk",
        # "id": "blue_ladders_store"
        # }
        # result = braintree.MerchantAccount.create(merchant_account_params)

        # result = braintree.Transaction.sale({
        #     "amount": "100.00",
        #     "merchant_account_id": "1234569646845",
        #     "credit_card": {
        #         "number": "4111111111111111",
        #         "expiration_date": "05/2016",
        #         "cvv": "100"
        #     },
        #     "options": {
        #     "submit_for_settlement": True,
        #     "hold_in_escrow": True,
        #     },
        #     "service_fee_amount": "10.00"
        # })
        #
        # transaction = result.transaction
        # print transaction.id
        # result = braintree.Transaction.release_from_escrow("8jqc5y")
        # print result
        # transaction = braintree.Transaction.find("bt2g8t")
        # print transaction.escrow_status


class LoginView(TemplateView, View):
    template_name = 'accounts/login.html'

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context['form'] = AuthenticationForm()
        if 'form' in kwargs:
            context.update({'form': AuthenticationForm(data=self.request.POST)})
        return context

    def get(self, request):
        if request.user.is_authenticated():
            return HttpResponseRedirect('/')
        return self.render_to_response(self.get_context_data())

    def post(self, request):
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            login(request, form.get_user())
            return HttpResponseRedirect('/list')
        else:
            return self.render_to_response(self.get_context_data(form=form))


class RegisterView(TemplateView, View):
    template_name = 'accounts/registr.html'

    def get_context_data(self, **kwargs):
        data = {}
        context = super(RegisterView, self).get_context_data(**kwargs)
        context['form'] = RegistrationForm()
        if 'form' in kwargs:
            context.update({'form': RegistrationForm(self.request.POST)})
        return context

    def get(self, request,*args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect('/')
        return self.render_to_response(self.get_context_data())

    def post(self, request):
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = User()
            user.email = form.cleaned_data['email']
            user.role = 'client'
            user.first_name = form.cleaned_data['first_name']
            user.phone_number = form.cleaned_data['phone_number']
            user.last_name = form.cleaned_data['last_name']
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "Your request has been sent successfully")
            return HttpResponseRedirect('/')
        else:
            return self.render_to_response(self.get_context_data(form=form))


class LogoutView(TemplateView):
    template_name = 'accounts/home.html'

    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/')

def save_profile(backend, user, response, *args, **kwargs):
    data = {}
    data['is_social'] = True
    if backend.name == 'facebook':
        if kwargs['is_new']:
            data['first_name'] = kwargs['details']['first_name']
            data['last_name'] = kwargs['details']['last_name']
            data['email'] = kwargs['details']['email']
            register_form = SocialForm(data=data)
            if register_form.is_valid():
                new_user_instance = User.objects.get(email=kwargs['details']['email'])
                if not kwargs['details']['email']:
                    new_user_instance = User()
                    new_user_instance.first_name = kwargs['details']['first_name']
                    new_user_instance.email = kwargs['details']['email']
                    new_user_instance.last_name = kwargs['details']['last_name']
                    new_user_instance.is_active = 1
                    new_user_instance.save()
                else:
                    new_user_instance = new_user_instance
                return {
                    'is_new': True,
                    'user': new_user_instance
                }
            else:

                backend.strategy.session_set('social_data', data)

                return HttpResponseRedirect('/registration/')

    elif backend.name == 'google-oauth2':
        if kwargs['is_new']:
            data['first_name'] = kwargs['details']['first_name']
            data['last_name'] = kwargs['details']['last_name']
            data['email'] = kwargs['details']['email']
            register_form = SocialForm(data=data)
            if register_form.is_valid():
                new_user_instance = User.objects.get(email=kwargs['details']['email'])
                if not kwargs['details']['email']:
                    new_user_instance = User()
                    new_user_instance.first_name = kwargs['details']['first_name']
                    new_user_instance.email = kwargs['details']['email']
                    new_user_instance.last_name = kwargs['details']['last_name']
                    new_user_instance.is_active = 1
                    new_user_instance.save()
                else:
                    new_user_instance = new_user_instance
                return {
                    'is_new': True,
                    'user': new_user_instance
                }
            else:

                backend.strategy.session_set('social_data', data)

                return HttpResponseRedirect('/registration/')



class ResetView(TemplateView, View):
    template_name = 'accounts/reset.html'

    def get_context_data(self, **kwargs):
        context = super(ResetView, self).get_context_data(**kwargs)
        if 'form' not in kwargs:
            context.update({'form': ResetForm()})
        return context

    def get(self, request):
        if request.user.is_authenticated():
            return HttpResponseRedirect('/')
        return self.render_to_response(self.get_context_data())

    def post(self, request):
        form = ResetForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            reset_key = generate_activation_key(email)
            user = User.objects.get(email=email)
            user.reset_key = reset_key
            user.save()
            reset_mail(request, email, user.first_name, reset_key)
            messages.success(request, "Please check your email address for change your account password")
            return HttpResponseRedirect('/')
        else:
            return self.render_to_response(self.get_context_data(form=form))


class ChangePasswordView(TemplateView, View):
    template_name = 'accounts/change_password.html'

    def get_context_data(self, **kwargs):
        context = super(ChangePasswordView, self).get_context_data(**kwargs)
        if 'form' not in kwargs:
            context.update({'form': ChangePasswordForm()})
        if 'reset_key' in kwargs:
            context['reset_key'] = kwargs['reset_key']
        return context

    def get(self, request, reset_key):
        if request.user.is_authenticated():
            return HttpResponseRedirect('/')
        try:
            user = User.objects.get(reset_key=reset_key)
            return self.render_to_response(self.get_context_data(reset_key=reset_key))
        except:
            messages.error(request, "Sorry, key is invalid")
            return HttpResponseRedirect('/')

    def post(self, request, reset_key):
        form = ChangePasswordForm(data=request.POST)
        if form.is_valid():
            try:
                reset_key = reset_key
                user = User.objects.get(reset_key=reset_key)
                user.reset_key = None
                user.set_password(form.cleaned_data['password'])
                user.save()
                messages.success(request, "Your password has been successfully changed")
            except:
                messages.success(request, "Sorry, there are some problems")
            return HttpResponseRedirect('/')
        else:
            return self.render_to_response(self.get_context_data(form=form))


def error404(request):
    return render(request, '404.html')