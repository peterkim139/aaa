import datetime
import braintree
import json
from django.db.models import Q
from django.http import JsonResponse
from decimal import Decimal
from django.utils import timezone
from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.utils.html import strip_tags
from django.core import serializers
from django.http import HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.core.cache import cache
from payment.models import Rent
from django.http import Http404
from .forms import RentForm, SupportForm
from accounts.forms import BillingForm
from accounts.models import User, Billing
from category.models import Params
from accounts.mixins import LoginRequiredMixin
from payment.generate import NemoEncrypt
from pages.utils import date_handler, save_file, refund_price, handel_datetime, utc_to_local, get_timezone
from payment.utils import payment_connection, cancel_transaction, seller_approve, show_errors, create_customer, check_user_card
from pages.emails import seller_approved_request, new_message,seller_declined_request, cancel_before_approving, cancel_after_approving, seller_penalize_email, seller_canceled_request_before, seller_canceled_request_after, send_support_email
from pages.models import Image, Thread, Message, Image

class OutTransactionsView(LoginRequiredMixin, TemplateView):

    template_name = 'pages/out_transactions.html'

    def get_context_data(self, data, **kwargs):

            context = super(OutTransactionsView, self).get_context_data(out_transactions=data, **kwargs)
            context['form'] = RentForm()
            return context

    def get(self, request):
        handel_datetime(request)

        if 'name' in request.GET:
            name = request.GET['name']
            if name == 'DESC':
                order = '-param__name'
            else:
                order = 'param__name'
        else:
            order = '-created'

        out_transactions = Rent.objects.filter(user_id=request.user.id) \
            .select_related('param', 'param__image')\
            .order_by(order)
        hour = timezone.now() - datetime.timedelta(hours=2)
        for out_transaction in out_transactions:
            if out_transaction.modified < hour:
                out_transaction.cancel = 1
            else:
                out_transaction.cancel = 0

        paginator = Paginator(out_transactions, 10)
        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        return self.render_to_response(self.get_context_data(posts))

    def post(self, request):
        handel_datetime(request)

        if request.POST['rent']:
            payment_connection()
            rent = int(request.POST['rent'])
            if request.POST['action'] == 'Decline':
                status = 'customer_declined'
            else:
                status = 'customer_canceled'
            requests = Rent.objects.get(user_id=request.user.id, id=rent)
            if requests.status == 'pending' or requests.status == 'approved':
                encrypt = NemoEncrypt()
                current_user = User.objects.get(id=requests.owner_id)
                orderer = User.objects.get(id=requests.user_id)
                item = Params.objects.get(id=requests.param_id)
                if status == 'customer_declined':
                    Rent.objects.filter(user_id=request.user.id, id=rent).update(status=status)
                    cancel_before_approving(request, current_user.email, orderer.first_name, current_user.first_name, item.name)
                    return JsonResponse({'success': True, 'message': 'Request has been declined'})
                else:
                    today = timezone.now() + datetime.timedelta(days=1)
                    paid = refund_price(requests.price)
                    if today < requests.start_date:
                        result = cancel_transaction(paid['amount'], orderer)
                        if result.is_success:
                            Rent.objects.filter(user_id=request.user.id, id=rent).update(status=status)
                            credits = Decimal(current_user.credits) + Decimal(paid['credit'])
                            User.objects.filter(id=current_user.id).update(credits=credits)
                            cancel_after_approving(request, current_user.email, orderer.first_name, item.name, current_user.first_name, paid['credit'])
                            return JsonResponse({'success': True, 'message': 'Request has been canceled'})
                        else:
                            return JsonResponse({'success': False, 'message': 'There is an error in refund process'})
            else:
                messages.error(request, "There is no request")
        else:
            messages.error(request, "There is no request")
        return HttpResponseRedirect('/profile/out_transactions/')


class InTransactionsView(LoginRequiredMixin, TemplateView):

    template_name = 'pages/in_transactions.html'

    def get_context_data(self, data, **kwargs):
            context = super(InTransactionsView, self).get_context_data(in_transactions=data, **kwargs)
            context['form'] = RentForm()
            return context

    def get(self, request):
        handel_datetime(request)

        if 'name' in request.GET:
            name = request.GET['name']
            if name == 'DESC':
                order = '-param__name'
            else:
                order = 'param__name'
        else:
            order = '-created'

        in_transactions = Rent.objects\
            .filter(owner_id=request.user.id)\
            .select_related('user', 'param', 'param__image')\
            .order_by(order)

        today = timezone.now() + datetime.timedelta(days=1)
        for in_transaction in in_transactions:
            if today < in_transaction.start_date:
                in_transaction.param.amount = '2'
            else:
                in_transaction.param.amount = '5'

        paginator = Paginator(in_transactions, 10)
        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        return self.render_to_response(self.get_context_data(posts))

    def post(self, request):
        handel_datetime(request)

        if request.POST['rent']:
            payment_connection()
            rent = int(request.POST['rent'])
            requests = Rent.objects.get(owner_id=request.user.id, id=rent)
            if request.POST['action'] == 'Approve':
                status = 'approved'
            elif request.POST['action'] == 'Cancel' and requests.status == 'pending':
                status = 'seller_declined'
            else:
                status = 'seller_canceled'

            if requests.status == 'pending' or requests.status == 'approved':
                encrypt = NemoEncrypt()
                current_user = User.objects.get(id=requests.owner_id)
                orderer = User.objects.get(id=requests.user_id)
                if status == 'approved':
                    customer_id = encrypt.decrypt_val(orderer.customer_id)
                    twoplaces = Decimal(10) ** -2
                    fee = Decimal(requests.price)*Decimal(12.9/100)+Decimal('0.30')
                    fee = fee.quantize(twoplaces)
                    result = seller_approve(requests, current_user, customer_id, fee)
                    if result.is_success:
                        transaction = result.transaction
                        Rent.objects.filter(owner_id=request.user.id, id=rent).update(transaction=transaction.id, status=status, modified=timezone.now())
                        seller_approved_request(request, orderer.first_name, current_user.first_name, orderer.email, requests.param.name, requests.price, requests.param.id, current_user.id)
                        return JsonResponse({'success': True, 'message': 'The request has been approved'})
                    else:
                        return JsonResponse({'success': False, 'message': 'There are some errors in transaction process'})

                elif status == 'seller_declined':
                    Rent.objects.filter(owner_id=request.user.id, id=rent).update(status=status)
                    seller_declined_request(request, orderer.first_name, orderer.email, requests.param.name, requests.param.subcategory_id)
                    return JsonResponse({'success': True, 'message': 'The request has been declined'})

                elif status == 'seller_canceled':
                    form = RentForm(data=request.POST)
                    if form.is_valid():
                        expiration_date = form.cleaned_data['month'] + '/' + form.cleaned_data['year']
                        customer = create_customer(request,form,expiration_date)
                        if customer.is_success:
                            today = timezone.now() + datetime.timedelta(days=1)
                            customer_id = customer.customer.id
                            if today < requests.start_date:
                                amount = '2.00'
                            else:
                                amount = '5.00'

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
                                    item = Params.objects.get(id=requests.param_id)
                                    seller_penalize_email(request, current_user.first_name, item.name, amount, current_user.email)
                                    if amount == '2.00':
                                        seller_canceled_request_before(request, orderer.first_name, orderer.email, requests.param.name)
                                    else:
                                        credits = Decimal(orderer.credits) + Decimal('2.00')
                                        User.objects.filter(id=orderer.id).update(credits=credits)
                                        seller_canceled_request_after(request, orderer.first_name, orderer.email, requests.param.name)
                                    messages.success(request, "Request has been canceled")
                                    Rent.objects.filter(owner_id=request.user.id, id=rent).update(status=status)
                                else:
                                    messages.error(request, "There is an error in refund process")
                            else:
                                show_errors(request, refund)
                        else:
                            show_errors(request, customer)
                    else:
                        return self.render_to_response(self.get_context_data(form=form))
            else:
                messages.error(request, "There is no request")
        else:
            messages.error(request, "There is no request")

        return HttpResponseRedirect('/profile/in_transactions/')

class RentPaymentView(LoginRequiredMixin, View):

    def get(self,request):
        raise Http404

    def post(self, request):
        form = BillingForm(request.POST)
        item_id = request.POST['item_id']
        response = HttpResponseRedirect('/payment/rent/'+item_id)
        if form.is_valid():
            payment_connection()
            expiration_date = form.cleaned_data['month'] + '/' + form.cleaned_data['year']
            result = check_user_card(form, expiration_date)
            if result.is_success:
                transaction = result.transaction
                braintree.Transaction.void(transaction.id)
            else:
                messages.error(request, "Credit card is invalid")
                response.set_cookie('billing', 'error', max_age=10)
                return response
            customer = create_customer(request, form, expiration_date)
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
                messages.success(request, "Payment added successfully.")
            else:
                show_errors(request, customer)
                response.set_cookie('billing', 'error',max_age=10)
        else:
            response.set_cookie('billing', 'error', max_age=10)
            cache.set('billing_error', BillingForm(request.POST))

        return response

class UploadImageView(LoginRequiredMixin, View):

    def post(self, request):
        if request.method == "POST":
            if request.is_ajax():
                upload = request
                filename = request.GET['qqfile']
                print filename
                response = save_file(request, upload, filename, 'images/items/', True)
            return JsonResponse({'filename': response})


class ChangeListingStatusView(LoginRequiredMixin, View):

    def post(self, request):
        item_id = request.POST['item_id']
        status = request.POST['status']
        try:
            param = Params.objects.get(id=item_id)
        except Params.DoesNotExist:
            param = None
        if param and param.item_owner_id == request.user.id:
            param.status = status
            param.save()
            return JsonResponse({'response': True})
        else:
            return JsonResponse({'response': False})


class UnreadMessagesView(LoginRequiredMixin, View):

    def post(self, request):

        partner_id = request.POST["partner_id"]
        item_id = request.POST["item_id"]
        try:
            thread = Thread.objects.get(Q(user1_id=request.user.id, user2_id=partner_id, item_id_id=item_id) | Q(user1_id=partner_id, user2_id=request.user.id, item_id_id=item_id))
            thread_id = thread.id
            unread_messages = (Message.objects.filter(thread_id=thread_id, from_user_id=partner_id, unread=1)
                               .values('id', 'message','modified', 'from_user_id__photo', 'thread_id','from_user_id_id'))

            if not unread_messages:
                return JsonResponse({'response': False})
            else:
                previous = None
                get_last_read = (Message.objects.filter(thread_id=thread.id, unread=0)
                                .values('id', 'message', 'modified', 'from_user_id_id').order_by('-id'))
                if get_last_read and get_last_read[0]['from_user_id_id'] != request.user.id:
                    previous = get_last_read['modified']
                for unread_message in unread_messages:
                    if previous:
                        if (unread_message['modified'] - previous).total_seconds() < 60:
                            unread_message['thread_id'] = 0
                    unread_message['modified'] = utc_to_local(unread_message['modified'] ,get_timezone(request))
                    previous = unread_message['modified']
                    unread_message['modified'] = unread_message['modified'].strftime("%B %d, %Y %I:%M%p")

                message_data = json.dumps(list(unread_messages), date_handler(unread_messages))
                messages = Message.objects.filter(thread_id=thread_id, from_user_id=partner_id, unread=1)
                for message in messages:
                    message.unread = 0
                    message.save()
                return HttpResponse(message_data, content_type="application/json")
        except Thread.DoesNotExist:
            return JsonResponse({'response': False})


class NoConversationView(LoginRequiredMixin, View):

    def get(self, request):

        try:
            user = Thread.objects.filter(Q(user1_id=request.user.id) | Q(user2_id=request.user.id)).order_by('-modified').first()
        except Thread.DoesNotExist:
            user = None
        if user:
            if user.user1_id == request.user.id:
                partner_id = user.user2_id
            else:
                partner_id = user.user1_id
            return HttpResponseRedirect('/profile/conversation/'+str(partner_id) + '/' + str(user.item_id_id))
        else:
            return render(request, 'pages/no_conversation.html')

class StartChatView(LoginRequiredMixin, View):

    def post(self, request):
        partner_id = request.POST["partner_id"]
        item_id = request.POST["item_id"]
        current_user_id = request.user.id
        messages = None
        try:
            thread = Thread.objects.get(Q(user1_id=request.user.id, user2_id=partner_id, item_id_id=item_id) | Q(user1_id=partner_id, user2_id=request.user.id, item_id_id=item_id))
        except Thread.DoesNotExist:
            thread = None
        if thread:
            messages = (Message.objects.filter(thread_id=thread.id)
                        .values('id', 'message', 'modified', 'from_user_id_id', 'from_user_id__photo', 'thread_id'))
            unread_messages = Message.objects.filter(thread_id=thread.id,from_user_id=partner_id,unread=1)
            for unread_message in unread_messages:
                unread_message.unread = 0
                unread_message.save()

        else:
            thread = Thread()
            thread.user1_id = request.user.id
            thread.user2_id = partner_id
            thread.item_id_id = item_id
            thread.last_message = ""
            thread.save()
        user = User.objects.filter(id=partner_id)
        item = Image.objects.filter(param_image_id=item_id)
        response_data = {}
        response_data['user'] = {}
        response_data['user']['user_name'] = user[0].first_name + ' ' + user[0].last_name
        response_data['user']['partner_id'] = user[0].id
        response_data['user']['user_id'] = current_user_id
        response_data['user']['current_user_name'] = request.user.first_name
        response_data['user']['current_user_last'] = request.user.last_name
        response_data['user']['photo'] = user[0].photo.name or 'images/users/default_user_photo.jpg'
        response_data['user']['my_photo'] = request.user.photo.name or 'images/users/default_user_photo.jpg'
        response_data['item'] = serializers.serialize('json', item)
        response_data['thread_id'] = thread.id
        if messages is not None:
            for message in messages:
                message['modified'] = utc_to_local(message['modified'], get_timezone(request))
                message['modified'] = message['modified'].strftime("%B %d, %Y %I:%M%p")
        else:
            messages = []

        message_data = json.dumps(list(messages), date_handler(messages))
        response_data['messages'] = message_data
        return HttpResponse(JsonResponse(response_data), content_type="application/json")


class ConversationView(LoginRequiredMixin, View):

    def get(self, request, id, item):
        handel_datetime(request)
        partner_id = id
        messages = None
        current_user_id = request.user.id
        image = Image.objects.get(param_image_id=item)
        itemInfo = Params.objects.get(id=item)
        try:
            thread = Thread.objects.get(Q(user1_id=request.user.id, user2_id=partner_id, item_id_id=item) | Q(user1_id=partner_id, user2_id=request.user.id, item_id_id=item))
        except Thread.DoesNotExist:
            thread = None
        if thread:
            messages = Message.objects.filter(thread_id=thread.id)
            unread_messages = Message.objects.filter(thread_id=thread.id,from_user_id=partner_id,unread=1)
            for unread_message in unread_messages:
                unread_message.unread = 0
                unread_message.save()
        else:
            thread = Thread()
            thread.user1_id = request.user.id
            thread.user2_id = partner_id
            thread.last_message = ""
            thread.save()

        threads = Thread.objects.raw('''
            SELECT *,COUNT(message.id) AS message_count,user.email as email,user.photo as user_photo, user.id as user_id, user.first_name as user_first_name, user.last_name as user_last_name FROM thread
            LEFT JOIN user
            ON (user.id=thread.user1_id AND thread.user1_id!=%s) OR (user.id=thread.user2_id AND thread.user2_id!=%s)
            LEFT JOIN message
            ON message.thread_id = thread.id AND message.unread = 1 AND message.to_user_id_id = %s
            WHERE thread.user1_id=%s OR thread.user2_id=%s
            GROUP BY thread.id
            ORDER BY thread.modified DESC''',
                 [current_user_id, current_user_id, current_user_id, current_user_id, current_user_id])

        previous = None
        if messages is not None:
            for message in messages:
                if previous:
                    if previous.from_user_id_id == message.from_user_id_id and (message.created - previous.created).total_seconds() < 60 :
                        message.message = previous.message + ' <br/> ' +  message.message
                        previous.bubble = True
                previous = message
            context = {'threads': threads, 'messages': messages, 'item_image': image, 'partner_id': partner_id, 'item_id':item, 'item' : itemInfo}
        else:
            context = {'threads': threads, 'item_image': image, 'partner_id': partner_id, 'item_id':item, 'item' : itemInfo}

        return render(request, 'pages/conversation.html', context)

    def post(self, request, id, item):
        handel_datetime(request)
        partner_id = id
        user_partner = User.objects.get(id=partner_id)
        last_message = strip_tags(request.POST["message"])
        message_time = timezone.localtime(timezone.now())
        if last_message != '' and len(last_message) <= 250:
            try:
                thread = Thread.objects.get(Q(user1_id=request.user.id, user2_id=partner_id, item_id_id=item) | Q(user1_id=partner_id, user2_id=request.user.id, item_id_id=item))
                thread.last_message = last_message
                thread.modified = message_time
                thread.save()
            except Thread.DoesNotExist:
                thread = Thread()
                thread.user1_id = request.user.id
                thread.user2_id = partner_id
                thread.item_id_id = item
                thread.last_message = last_message
                thread.modified = message_time
                thread.save()

            try:
                get_last_writer = Message.objects.filter(from_user_id_id=request.user.id, to_user_id_id=partner_id, thread_id=thread.id).order_by('-id')[0]
            except IndexError:
                get_last_writer = None

            message = Message()
            message.thread_id = thread.id
            message.unread = 1
            message.message = last_message
            message.from_user_id = User.objects.get(id=request.user.id)
            message.to_user_id = User.objects.get(id=partner_id)
            message.save()
            new_message(request, user_partner.email, user_partner.first_name, thread.item_id.name, last_message, item)
            bubble = False
            if get_last_writer and get_last_writer.from_user_id_id == request.user.id and (message.created - get_last_writer.created).total_seconds() < 60:
                bubble = True
            return JsonResponse({'response': True, 'modified': message_time.strftime("%B %d, %Y %I:%M%p"),'last_message':last_message,'bubble':bubble})
        else:
            return JsonResponse({'response': False})

class UserStatusView(LoginRequiredMixin, View):

    def post(self, request):

        current_user_id = request.user.id
        threads = Thread.objects.raw('''
            SELECT *, COUNT(message.id) AS message_count
            FROM thread
            LEFT JOIN message
              ON message.thread_id = thread.id AND message.unread = 1 AND message.to_user_id_id = %s
            WHERE thread.user1_id=%s OR thread.user2_id=%s
            GROUP BY thread.id
            HAVING message_count > 0
            ORDER BY thread.modified DESC''',
            [current_user_id, current_user_id, current_user_id])

        final = []
        for t in threads:
            status_data = {}
            if(t.user1_id == current_user_id):
                status_data['id'] = t.user2_id
            else:
                status_data['id'] = t.user1_id

            status_data['item_id'] = t.item_id_id
            status_data['message_count'] = t.message_count
            status_data['message_text'] = t.last_message
            # status_data['online'] = t.online(t.email)
            final.append(status_data)

        status_list = json.dumps(final)
        return HttpResponse(status_list, content_type="application/json")

class SupportView(View):

    def get(self, request):
        form = SupportForm()
        context = {'form': form}
        return render(request, 'pages/support.html', context)

    def post(self, request):
        form = SupportForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            name = form.cleaned_data['name']
            comments = form.cleaned_data['comments']
            if send_support_email(email, name, comments):
                messages.success(request, "Your message has been sent successfully")
            else:
                messages.error(request, "Your message could not be sent")
            return HttpResponseRedirect('/profile/support/')
        else:
            context = {'form': form}
            return render(request, 'pages/support.html', context)




