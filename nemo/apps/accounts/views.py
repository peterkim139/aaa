import datetime
import json
import os
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
from .forms import ProfileForm,RegistrationForm,AuthenticationForm,ResetForm,ChangePasswordForm,SocialForm
from accounts.mixins import LoginRequiredMixin
from accounts.utils import get_coordinates,generate_activation_key,reset_mail, confirm_register_mail
from django.conf import settings
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from accounts.models import User
from category.models import Params, SubCategory
import braintree
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class HomeView(View):
    def get(self, request):
        cats = SubCategory.objects.all()

        coordinates = get_coordinates(request)
        latitude = coordinates[0]
        longitude = coordinates[1]
        limit = 10

        items = Params.objects.raw('''SELECT *,(((ACOS(SIN(%s * PI() / 180) * SIN(parametrs.latitude * PI() / 180) + COS(%s * PI() / 180) * COS(parametrs.latitude * PI() / 180) * COS((%s - parametrs.longitude) * PI() / 180)) * 180 / PI()) * 60 * 1.1515)) AS distance FROM parametrs
                LEFT JOIN images
                ON images.param_image_id=parametrs.id
                ORDER BY distance ASC
                LIMIT %s''',
                [latitude, latitude, longitude, limit])

        count = len(list(items))
        context = {'items': items, 'cats': cats, 'count':count, 'latitude':latitude, 'longitude':longitude }
        return render(request, 'accounts/home.html', context)

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
            if request.GET and request.GET['next']:
                return HttpResponseRedirect(request.GET['next'])
            else:
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
            user.zip_code = form.cleaned_data['zip_code']
            user.last_name = form.cleaned_data['last_name']
            user.set_password(form.cleaned_data['password'])
            user.save()
            confirm_register_mail(request, user.email, user.first_name, user.last_name, user.zip_code)
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
                new_user_instance = User.objects.filter(email=kwargs['details']['email'])
                if not new_user_instance:
                    new_user_instance = User()
                    new_user_instance.first_name = kwargs['details']['first_name']
                    new_user_instance.email = kwargs['details']['email']
                    new_user_instance.last_name = kwargs['details']['last_name']
                    new_user_instance.is_active = 1
                    new_user_instance.save()
                else:
                    new_user_instance = User.objects.get(email=kwargs['details']['email'])
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
                new_user_instance = User.objects.filter(email=kwargs['details']['email'])
                if not new_user_instance:
                    new_user_instance = User()
                    new_user_instance.first_name = kwargs['details']['first_name']
                    new_user_instance.email = kwargs['details']['email']
                    new_user_instance.last_name = kwargs['details']['last_name']
                    new_user_instance.is_active = 1
                    new_user_instance.save()
                else:
                    new_user_instance = User.objects.get(email=kwargs['details']['email'])
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
            first_name = user.first_name
            reset_mail(request, email,first_name, reset_key)
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

class SearchView(View):

    def get(self, request):

        cats = SubCategory.objects.all()
        categories = request.GET.getlist('category')
        checked_categories = []
        for checked_category in categories:
            checked_categories.append(long(checked_category))

        if len(list(categories)) == 0:
            categories = list(cats.values_list('id', flat=True))
            checked_categories = ''

        expensive_item = Params.objects.all().order_by('-price')[:1]
        max_price = expensive_item[0].price

        query = request.GET.get("name")

        if request.GET.get("start_range"):
            start_range = request.GET.get("start_range")
        else:
            start_range = 0
        if request.GET.get("end_range"):
            end_range = request.GET.get("end_range")
        else:
            end_range = max_price

        coordinates = get_coordinates(request)
        latitude = coordinates[0]
        longitude = coordinates[1]

        items = Params.objects.raw('''SELECT *,(((ACOS(SIN(%s * PI() / 180) * SIN(parametrs.latitude * PI() / 180) + COS(%s * PI() / 180) * COS(parametrs.latitude * PI() / 180) * COS((%s - parametrs.longitude) * PI() / 180)) * 180 / PI()) * 60 * 1.1515)) AS distance FROM parametrs
                LEFT JOIN images
                ON images.param_image_id=parametrs.id
                WHERE (parametrs.name LIKE %s or parametrs.description LIKE %s)
                and parametrs.subcategory_id IN %s
                and parametrs.price >= %s and parametrs.price <= %s
                ORDER BY distance ASC''',
                [latitude, latitude, longitude, '%' + query + '%','%' + query + '%', categories, start_range, end_range])

        count = len(list(items))
        context = {'longitude':longitude,'latitude':latitude,'items': items,'cats': cats, 'count':count, 'checked_categories':checked_categories,'max_price': max_price }
        return render(request, 'accounts/search_results.html', context)

class ProfileView(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'accounts/profile.html')

class EditProfileView(LoginRequiredMixin, View):

    def get(self, request):
        form = ProfileForm(initial={'first_name': request.user.first_name,
                                    'last_name': request.user.last_name,
                                    'email': request.user.email,
                                    'phone_number': request.user.phone_number,
                                    'zip_code': request.user.zip_code})
        context = {'form': form }
        return render(request, 'accounts/edit_profile.html', context)

    def post(self, request):
        request.POST['user'] = request.user.id
        form = ProfileForm(request.POST,request.FILES)
        if form.is_valid():
            user = User.objects.get(id=request.user.id)
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.phone_number = form.cleaned_data['phone_number']
            user.zip_code = form.cleaned_data['zip_code']
            if 'image_file' in request.FILES:
                user.photo = request.FILES['image_file']
            user.save()
            messages.success(request,"Successfully Added")
            return HttpResponseRedirect('/profile/')
        else:
            context = {'form':form }
            return render(request, 'accounts/edit_profile.html', context)

def error404(request):
    return render(request, '404.html')