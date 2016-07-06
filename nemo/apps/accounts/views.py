from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.contrib.auth import login, authenticate,logout
from django.http import HttpResponseRedirect
from django.core.cache import cache
from django.contrib import messages
from django.core import serializers
from .forms import ProfileForm, RegistrationForm, AuthenticationForm, ResetForm, ChangePasswordForm, SocialForm, BillingForm
from accounts.mixins import LoginRequiredMixin
from accounts.utils import get_coordinates, generate_activation_key
from accounts.emails import reset_mail, confirm_register_mail
from payment.generate import NemoEncrypt
from accounts.models import User, Billing
from category.models import Params, SubCategory, Category
from pages.models import Image
from pages.forms import AddListingForm
import braintree
import datetime
from payment.utils import show_errors, payment_connection, create_customer, check_user_card
from django.http import HttpResponse


class HomeView(View):
    def get(self, request):

        cats = SubCategory.objects.all()
        categories = Category.objects.all()
        coordinates = get_coordinates(request)
        latitude = coordinates[0]
        longitude = coordinates[1]
        limit = 10
        items = Params.objects.raw('''SELECT *,images.image_name as image_name, (((ACOS(SIN(%s * PI() / 180) * SIN(parametrs.latitude * PI() / 180) + COS(%s * PI() / 180) * COS(parametrs.latitude * PI() / 180) * COS((%s - parametrs.longitude) * PI() / 180)) * 180 / PI()) * 60 * 1.1515)) AS distance
                FROM parametrs
                LEFT JOIN images
                ON images.param_image_id=parametrs.id
                LEFT JOIN user
                ON user.id=parametrs.item_owner_id
                WHERE parametrs.status = 'published'
                AND user.profile_status=1
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
                AND user.profile_status=1
                ORDER BY parametrs.created DESC
                LIMIT 5''')

        context = {'items': items, 'recent_items': recent_items, 'categories':categories, 'cats': cats, 'count': count, 'latitude': latitude, 'longitude': longitude}
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
            if request.GET and request.GET['next']:
                response.set_cookie('next', request.GET['next'])
            return response


class RegisterView(View):

    def post(self, request):
        
        form = RegistrationForm(data=request.POST)
        response = HttpResponseRedirect('/')
        if form.is_valid():
            user = User()
            year = request.POST['birthdate_year']
            month = request.POST['birthdate_month']
            day = request.POST['birthdate_day']
            date_of_birth = year+'-'+month+'-'+day
            user.birthday = date_of_birth
            user.email = form.cleaned_data['email']
            user.role = 'client'
            user.first_name = form.cleaned_data['first_name']
            user.phone_number = form.cleaned_data['phone_number']
            user.zip_code = form.cleaned_data['zip_code']
            user.last_name = form.cleaned_data['last_name']
            user.set_password(form.cleaned_data['password'])
            user.save()
            confirm_register_mail(request, user.email, user.first_name, user.last_name, user.zip_code)
            new_user = authenticate(email=form.cleaned_data['email'],
                                    password=form.cleaned_data['password'],
                                    )
            login(request, new_user)
            messages.success(request, "You have registered successfully.")
        else:
            response.set_cookie('registr_error', 'error')
            cache.set('registartion_error', RegistrationForm(request.POST))

        return response


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
                    new_user_instance.profile_status = 1
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
                    new_user_instance.profile_status = 1
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


class ResetView(TemplateView):

    def post(self, request):
        form = ResetForm(data=request.POST)
        response = HttpResponseRedirect('/')
        if form.is_valid():
            email = form.cleaned_data['email']
            reset_key = generate_activation_key(email)
            user = User.objects.get(email=email)
            user.reset_key = reset_key
            user.save()
            first_name = user.first_name
            reset_mail(request, email, first_name, reset_key)
            messages.success(request, "The email has been sent! Please check your inbox for link to reset password.")
        else:
            response.set_cookie('forgot_error', 'error')
            cache.set('forgot_error', ResetForm(request.POST))

        return response


class ChangePasswordView(TemplateView):

    def get(self, request, reset_key):

        response = HttpResponseRedirect('/')
        if request.user.is_authenticated():
            return response
        try:
            User.objects.get(reset_key=reset_key)
            response.set_cookie('reset_key', reset_key)
        except User.DoesNotExist:
            response = HttpResponseRedirect('/')
            response.set_cookie('forgot_error', 'invalid_key')
            messages.error(request, "Sorry, key is invalid")
        return response

    def post(self, request, reset_key):
        form = ChangePasswordForm(data=request.POST)
        response = HttpResponseRedirect('/')
        if form.is_valid():
            try:
                reset_key = reset_key
                user = User.objects.get(reset_key=reset_key)
                user.reset_key = None
                user.set_password(form.cleaned_data['password'])
                user.save()
                new_user = authenticate(email=user.email,
                        password=form.cleaned_data['password'],
                        )
                login(request, new_user)
                messages.success(request, "Your password has been successfully changed")
            except User.DoesNotExist:
                messages.success(request, "Sorry, there are some problems")
            response.set_cookie('reset_key_error', 'clear')
            return response
        else:
            response.set_cookie('reset_error', 'error')
            cache.set('reset_error', ChangePasswordForm(request.POST))
            return response


class SearchView(View):

    def get(self, request):
        cats = SubCategory.objects.all()
        categories = request.GET.getlist('category')
        category_types = Category.objects.all()
        checked_categories = []
        for checked_category in categories:
            checked_categories.append(long(checked_category))

        if len(list(categories)) == 0:
            categories = list(cats.values_list('id', flat=True))
            checked_categories = ''

        try:
            expensive_item = Params.objects.all().order_by('-price')[:1]
        except Params.DoesNotExist:
            expensive_item = None
        if expensive_item:
            max_price = expensive_item[0].price
        else:
            max_price = 500

        if request.GET.get("name"):
            query = request.GET.get("name")
        else:
            query = ''

        if request.GET.get("start_range"):
            start_range = request.GET.get("start_range")
        else:
            start_range = 0
        if request.GET.get("end_range"):
            end_range = request.GET.get("end_range")
        else:
            end_range = max_price

        if request.GET.get("type"):
            cat_type = request.GET.get("type")
        else:
            cat_type = 1

        coordinates = get_coordinates(request)
        latitude = coordinates[0]
        longitude = coordinates[1]
        limit = 4
        if request.is_ajax():
            offset = request.session['offset']
            request.session['offset'] = offset + limit
        else:
            offset = 0
            request.session['offset'] = limit

        try:
            items = Params.objects.raw('''SELECT *,images.image_name as image_name,(((ACOS(SIN(%s * PI() / 180) * SIN(parametrs.latitude * PI() / 180) + COS(%s * PI() / 180) * COS(parametrs.latitude * PI() / 180) * COS((%s - parametrs.longitude) * PI() / 180)) * 180 / PI()) * 60 * 1.1515)) AS distance FROM parametrs
                LEFT JOIN images
                ON images.param_image_id=parametrs.id
                LEFT JOIN sub_category
                ON sub_category.id=parametrs.subcategory_id
                LEFT JOIN user
                ON user.id=parametrs.item_owner_id
                WHERE (parametrs.name LIKE %s or parametrs.description LIKE %s)
                and parametrs.subcategory_id IN %s
                and user.profile_status = 1
                and parametrs.price >= %s and parametrs.price <= %s
                and parametrs.status = 'published'
                and sub_category.category_id = %s
                ORDER BY distance ASC
                LIMIT %s
                OFFSET %s''',
                [latitude, latitude, longitude, '%' + query + '%', '%' + query + '%', categories, start_range, end_range, cat_type, limit, offset])
            count = len(list(items))
        except Params.DoesNotExist:
            count = 0

        if request.is_ajax():
            items = list(items)
            for item in items:
                item.city = item.distance
                item.address = item.image_name
                item.status = item.first_name.title()[0] + '.' + item.last_name.title()[0]+'.'

            items = serializers.serialize('json', list(items))
            return JsonResponse({'items': items, 'count': count, 'limit': limit, 'longitude': longitude, 'latitude': latitude}, safe=False)
        else:
            context = {'category_types': category_types,'longitude': longitude, 'latitude': latitude, 'items': items, 'cats': cats, 'count': count, 'limit': limit, 'checked_categories': checked_categories, 'max_price': max_price}
            return render(request, 'accounts/search_results.html', context)


class EditProfileView(LoginRequiredMixin, View):

    def get(self, request):
        form = ProfileForm(initial={'first_name': request.user.first_name,
                                    'last_name': request.user.last_name,
                                    'email': request.user.email,
                                    'phone_number': request.user.phone_number,
                                    'zip_code': request.user.zip_code})
        context = {'form': form}
        return render(request, 'accounts/edit_profile.html', context)

    def post(self, request):
        request.POST['user'] = request.user.id
        form = ProfileForm(request.POST, request.FILES)
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
            messages.success(request, "Successfully Edited")
            return HttpResponseRedirect('/edit_profile/')
        else:
            context = {'form': form}
            return render(request, 'accounts/edit_profile.html', context)


class BillingView(LoginRequiredMixin, View):

    def get(self, request):
        form = BillingForm()
        encrypt = NemoEncrypt()

        methods = Billing.objects.filter(user_id=request.user.id).order_by('-created')
        for method in methods:
            method.customer_number = encrypt.decrypt_val(method.customer_number)
        context = {'form': form, 'methods': methods}
        return render(request, 'accounts/billing.html', context)

    def post(self, request):
        form = BillingForm(request.POST)
        if form.is_valid():
            payment_connection()
            expiration_date = form.cleaned_data['month'] + '/' + form.cleaned_data['year']
            result = check_user_card(form, expiration_date)
            if result.is_success:
                transaction = result.transaction
                braintree.Transaction.void(transaction.id)
            else:
                messages.error(request, "Credit card is invalid")
                return HttpResponseRedirect('/billing/')
            customer = create_customer(request,form,expiration_date)
            if customer.is_success:
                encrypt = NemoEncrypt()
                customer_id = encrypt.encrypt_val(customer.customer.id)
                billing = Billing()
                billing.customer_id = customer_id
                billing.customer_name = form.cleaned_data['first_name']
                billing.customer_number = encrypt.encrypt_val(form.cleaned_data['card_number'])

                try:
                    def_method = Billing.objects.filter(user_id=request.user.id, is_default=1)
                except:
                    def_method = None
                if def_method:
                    Billing.objects.filter(user_id=request.user.id).update(is_default=0)

                billing.is_default = 1
                user = User.objects.get(id=request.user.id)
                user.customer_id = customer_id
                user.save()

                billing.user_id = request.user.id
                billing.save()
                if request.COOKIES.get('to_billing') is not None:
                    return HttpResponseRedirect('/payment/rent/'+request.COOKIES.get('to_billing'))
                messages.success(request, "Successfully Added")
            else:
                show_errors(request, customer)
            return HttpResponseRedirect('/billing/')
        else:
            encrypt = NemoEncrypt()
            methods = Billing.objects.filter(user_id=request.user.id)
            for method in methods:
                method.customer_number = encrypt.decrypt_val(method.customer_number)
            context = {'form': form, 'methods': methods}
            return render(request, 'accounts/billing.html', context)


class ChangeBillingStatusView(LoginRequiredMixin, View):

    def post(self, request):
        user_id = request.user.id
        method_id = int(request.POST['method_id'])
        status = int(request.POST['status'])
        try:
            method = Billing.objects.get(id=method_id, user_id=user_id)
        except Billing.DoesNotExist:
            method = None
        if method:
            user = User.objects.get(id=user_id)

            if status == 1:
                try:
                    def_method = Billing.objects.get(is_default=1, user_id=user_id)
                except Billing.DoesNotExist:
                    def_method = None
                if def_method:
                    def_method.is_default = 0
                    def_method.save()

                user.customer_id = method.customer_id
            else:
                user.customer_id = ''

            method.is_default = status
            method.save()
            user.save()
            return JsonResponse({'response': True})
        else:
            return JsonResponse({'response': False})


class DeleteBillingView(LoginRequiredMixin, View):

    def post(self, request):
        user_id = request.user.id
        method_id = int(request.POST['method_id'])
        try:
            method = Billing.objects.get(id=method_id, user_id=user_id)
        except Billing.DoesNotExist:
            method = None
        if method:
            is_default = method.is_default
            method.delete()
            if is_default == 1:
                user = User.objects.get(id=user_id)
                user.customer_id = ''
                user.save()
            return JsonResponse({'response': True})
        else:
            return JsonResponse({'response': False})


class ListingsView(LoginRequiredMixin, View):

    def get(self, request):

        listings = Params.objects.raw('''SELECT DISTINCT *, images.image_name as image_name, rent.status as rent_status,
                rent.start_date as rent_start_date, rent.rent_date as rent_end_date FROM parametrs
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
                AND parametrs.status!=%s''', [request.user.id, 'deleted'])

        form = AddListingForm()
        this_moment = datetime.datetime.now()
        context = {'listings': listings, 'this_moment': this_moment, 'form': form}
        return render(request, 'accounts/listings.html', context)

    def post(self, request):

        form = AddListingForm(request.POST, request.FILES)
        if form.is_valid():
            item_id = form.cleaned_data['item_id']
            if item_id and 'item_id' in request.session and item_id == request.session['item_id']:
                parameters = Params.objects.get(item_owner_id=request.user.id, id=item_id)
                image = Image.objects.get(param_image_id=item_id)
                message_text = "Successfully Edited"
                del request.session['item_id']
            else:
                message_text = "Successfully Added"
                parameters = Params()
                image = Image()
            parameters.price = form.cleaned_data['price']
            parameters.name = form.cleaned_data['name']
            parameters.item_owner_id = request.user.id
            parameters.subcategory = form.cleaned_data['subcategory']
            parameters.description = form.cleaned_data['description']
            parameters.address = form.cleaned_data['street_address']
            parameters.street = form.cleaned_data['street']
            parameters.city = form.cleaned_data['city']
            parameters.postal_code = form.cleaned_data['postal_code']
            parameters.state = form.cleaned_data['state']
            parameters.latitude = form.cleaned_data['latitude']
            parameters.longitude = form.cleaned_data['longitude']
            parameters.save()

            image_filename = ''
            if 'image_filename' in request.session:
                image_filename = request.session['image_filename']
            image_name = form.cleaned_data['image_file']
            if image_name == image_filename:
                image.image_name = image_name
                image.param_image_id = parameters.id
                image.save()
                del request.session['image_filename']

            messages.success(request, message_text)
            return HttpResponseRedirect('/listings/')
        else:
            context = {'form': form, 'val_error': 'true'}
            return render(request, 'accounts/listings.html', context)

class EditListingView(LoginRequiredMixin, View):

    def post(self, request):

        item_id = request.POST['item_id']
        param = Params.objects.get(item_owner_id=request.user.id, id=item_id)
        image = Image.objects.get(param_image_id=item_id)
        request.session['item_id'] = item_id
        return HttpResponse(serializers.serialize("json", [param,image]))


class ChangeAccountStatusView(LoginRequiredMixin, View):

    def post(self, request):
        user_id = request.user.id
        status = int(request.POST['status'])
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            user = None
        if user:
            user.profile_status = status
            user.save()
            return JsonResponse({'response': True})
        else:
            return JsonResponse({'response': False})


def error404(request):
    return render(request, '404.html')
