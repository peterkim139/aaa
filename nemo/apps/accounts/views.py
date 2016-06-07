import json
import os
import logging
from django.http import JsonResponse
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
from pages.models import Image
from payment.models import Rent
from pages.forms import AddListingForm
import braintree
import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class HomeView(View):
    def get(self, request):

        cats = SubCategory.objects.all()

        coordinates = get_coordinates(request)
        latitude = coordinates[0]
        longitude = coordinates[1]
        limit = 10
        items = Params.objects.raw('''SELECT *,images.image_name as image_name, (((ACOS(SIN(%s * PI() / 180) * SIN(parametrs.latitude * PI() / 180) + COS(%s * PI() / 180) * COS(parametrs.latitude * PI() / 180) * COS((%s - parametrs.longitude) * PI() / 180)) * 180 / PI()) * 60 * 1.1515)) AS distance FROM parametrs
                LEFT JOIN images
                ON images.param_image_id=parametrs.id
                LEFT JOIN user
                ON user.id=parametrs.item_owner_id
                WHERE parametrs.status = 'published'
                AND user.is_active=1
                ORDER BY distance ASC
                LIMIT %s''',
                [latitude, latitude, longitude, limit])

        count = len(list(items))

        recent_items = Params.objects.raw('''SELECT * FROM parametrs
                LEFT JOIN images
                ON images.param_image_id=parametrs.id
                LEFT JOIN user
                ON user.id=parametrs.item_owner_id
                WHERE parametrs.status = 'published'
                AND user.is_active=1
                ORDER BY parametrs.created DESC
                LIMIT 5''')

        context = {'items': items, 'recent_items': recent_items, 'cats': cats, 'count':count, 'latitude':latitude, 'longitude':longitude }
        return render(request, 'accounts/home.html', context)

class LoginView(View):

    def post(self, request):
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            login(request, form.get_user())
            if request.GET and request.GET['next']:
                return HttpResponseRedirect(request.GET['next'])
            else:
                return HttpResponseRedirect('/')
        else:
            response = HttpResponseRedirect('/')
            response.set_cookie('exist', 'error')
            return response


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

        try:
            expensive_item = Params.objects.all().order_by('-price')[:1]
        except:
            expensive_item = None
        if expensive_item:
            max_price = expensive_item[0].price
        else:
            max_price = 500


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
        limit = 8
        if request.is_ajax():
            offset = request.session['offset']
            request.session['offset'] = offset + limit
        else:
            offset = 0
            request.session['offset'] = limit

        try:
            items = Params.objects.raw('''SELECT *,(((ACOS(SIN(%s * PI() / 180) * SIN(parametrs.latitude * PI() / 180) + COS(%s * PI() / 180) * COS(parametrs.latitude * PI() / 180) * COS((%s - parametrs.longitude) * PI() / 180)) * 180 / PI()) * 60 * 1.1515)) AS distance FROM parametrs
                LEFT JOIN images
                ON images.param_image_id=parametrs.id
                LEFT JOIN user
                ON user.id=parametrs.item_owner_id
                WHERE (parametrs.name LIKE %s or parametrs.description LIKE %s)
                and parametrs.subcategory_id IN %s
                and user.is_active = 1
                and parametrs.price >= %s and parametrs.price <= %s
                and parametrs.status = 'published'
                ORDER BY distance ASC
                LIMIT %s
                OFFSET %s''',
                [latitude, latitude, longitude, '%' + query + '%','%' + query + '%', categories, start_range, end_range, limit, offset])
        except:
            items = None
        if items:
            count = len(list(items))
        else:
            count = 0

        if request.is_ajax():
            items = list(items)
            for item in items:
                item.address = item.image_name
                item.status = item.first_name.title()[0] +'.'+item.last_name.title()[0]+'.'

            items = serializers.serialize('json', list(items))
            return JsonResponse({'items':items,'count': count, 'limit':limit, 'longitude':longitude,'latitude':latitude}, safe=False)
        else:
            context = {'longitude':longitude,'latitude':latitude,'items': items,'cats': cats, 'count':count, 'limit':limit, 'checked_categories':checked_categories,'max_price': max_price }
            return render(request, 'accounts/search_results.html', context)

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
            messages.success(request,"Successfully Edited")
            return HttpResponseRedirect('/edit_profile/')
        else:
            context = {'form':form }
            return render(request, 'accounts/edit_profile.html', context)

class ListingsView(LoginRequiredMixin,View):

    def get(self, request):

        listings = Params.objects.raw('''SELECT DISTINCT *, images.image_name as image_name, rent.status as rent_status, rent.start_date as rent_start_date, rent.rent_date as rent_end_date FROM parametrs
                LEFT JOIN rent
                ON rent.param_id=parametrs.id AND rent.id =
                (
                   SELECT MAX(ren.id)
                   FROM rent ren
                   WHERE ren.param_id = parametrs.id AND ren.start_date <= CURDATE() AND ren.rent_date >= CURDATE()
                )
                LEFT JOIN images
                ON images.param_image_id=parametrs.id
                WHERE parametrs.item_owner_id = %s
                AND parametrs.status!=%s''',[request.user.id, 'deleted'])

        form = AddListingForm()
        this_moment = datetime.datetime.now()
        context = {'listings': listings, 'this_moment':this_moment,'form':form}
        return render(request, 'accounts/listings.html', context)


    def post(self, request):

        form = AddListingForm(request.POST, request.FILES)
        if form.is_valid():
            parameters = Params()
            parameters.price = form.cleaned_data['price']
            parameters.name = form.cleaned_data['name']
            parameters.item_owner_id = request.user.id
            parameters.subcategory = form.cleaned_data['subcategory']
            parameters.description = form.cleaned_data['description']
            parameters.address = form.cleaned_data['street_address']
            parameters.city = form.cleaned_data['city']
            parameters.postal_code = form.cleaned_data['postal_code']
            parameters.state = form.cleaned_data['state']
            parameters.latitude = form.cleaned_data['latitude']
            parameters.longitude = form.cleaned_data['longitude']
            parameters.save()

            image = Image()
            if 'image_filename' in request.session:
                image_filename = request.session['image_filename']
            image_name = form.cleaned_data['image_file']
            if image_name == image_filename:
                image.image_name = image_name
                image.param_image_id = parameters.id
                image.save()
                del request.session['image_filename']

            messages.success(request,"Successfully Added")
            return HttpResponseRedirect('/listings/')
        else:
            context = {'form': form, 'val_error':'true' }
            return render(request, 'accounts/listings.html', context)

class ChangeAccountStatusView(LoginRequiredMixin,View):

    def post(self, request):
        user_id = request.user.id
        status = int(request.POST['status'])
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            user = None
        if user:
            user.is_active = status
            user.save()
            return JsonResponse({'response':True})
        else:
            return JsonResponse({'response':False})


def error404(request):
    return render(request, '404.html')