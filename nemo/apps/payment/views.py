import datetime
import braintree
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.contrib import messages
from .forms import ConnectForm,RentForm
from accounts.mixins import LoginRequiredMixin
from django.db.models import Q
from .models import User,Params,Rent
from pages.models import Image
from payment.utils import payment_connection,show_errors
from payment.emails import new_rent_mail

class ConnectView(LoginRequiredMixin,TemplateView):
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
            if form.cleaned_data['phone_number']:
                phone = form.cleaned_data['phone_number']
            else:
                phone = request.user.phone_number
            merchant_account_params = {
            'individual': {
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
                'phone': phone,
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
                show_errors(request,result)
                return self.render_to_response(self.get_context_data(form=form))
        else:
            return self.render_to_response(self.get_context_data(form=form))



class RentView(TemplateView):
    template_name = 'payment/rent.html'
    item_id = ''
    def get_context_data(self, **kwargs):
        context = super(RentView, self).get_context_data(**kwargs)
        context['form'] = RentForm()
        blockdays = Rent.objects.filter(Q(status='pending',param_id=self.item_id) | Q(status='approved',param_id=self.item_id))
        dates = {}
        for blockday in blockdays:
            dates[ blockday.rent_date.strftime('%Y-%m-%d')] = blockday.start_date.strftime('%Y-%m-%d')
        context['blockdays'] = dates
        param = Params.objects.get(id=self.item_id,status='published',item_owner__is_active=1)
        image = Image.objects.get(param_image=self.item_id)
        today = datetime.datetime.now().date()
        try:
            rent = Rent.objects.get(status='approved',param_id = self.item_id,start_date__lte = today,rent_date__gte = today)
        except Rent.DoesNotExist:
            rent = None

        context['param'] = param
        context['rent'] = rent
        context['image'] = image
        if 'form' in kwargs:
            context.update({'form': RentForm(data=self.request.POST),'val_error':'true'})
        return context

    def get(self, request,item_id):
        self.item_id = item_id
        return self.render_to_response(self.get_context_data())

    def post(self, request,item_id):

        self.item_id = item_id
        form = RentForm(data=request.POST)
        if form.is_valid():

            blockdays = Rent.objects.filter(Q(status='pending',param_id=self.item_id) | Q(status='approved',param_id=self.item_id))
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

            current_user = User.objects.get(id=request.user.id)
            if current_user.customer_id:
                item = Params.objects.get(id=id)
                rent = Rent()
                rent.status = 'pending'
                rent.start_date = form.cleaned_data['start_date']
                rent.rent_date = form.cleaned_data['rent_date']
                start_date_str = str(rent.start_date)
                converted_start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d')
                rent_date_str = str(rent.rent_date)
                converted_rent_date = datetime.datetime.strptime(rent_date_str, '%Y-%m-%d')
                rent_period = converted_rent_date-converted_start_date
                rent.price = item.price*(rent_period.days+1)
                rent.owner_id = item.item_owner_id
                rent.param_id = item.id
                rent.user_id = request.user.id
                rent.save()
                seller = User.objects.get(id=item.item_owner_id)
                new_rent_mail(request,seller.email,request.user.first_name,item.name,seller.first_name,rent.id)
                messages.success(request, "Your request has been sent successfully")
                return HttpResponseRedirect('/payment/rent/'+id)
            else:
                messages.error(request, "Please add default payment method")
                return HttpResponseRedirect('/billing')

        else:
            return self.render_to_response(self.get_context_data(form=form))

