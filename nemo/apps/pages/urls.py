"""psdapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""

from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
     url(r'^change_listing_status/$',views.ChangeListingStatusView.as_view(),name='change_listing_status'),
     url(r'^upload_image/$',csrf_exempt(views.UploadImageView.as_view()),name='upload_image'),
     url(r'^in_transactions/$',views.InTransactionsView.as_view(),name='in_transactions'),
     url(r'^out_transactions/$',views.OutTransactionsView.as_view(),name='out_transactions'),
     url(r'^conversation/$',views.NoConversationView.as_view(),name='no_conversation'),
     url(r'^conversation/(?P<id>\d+)$',views.ConversationView.as_view(),name='conversation'),
     url(r'^unread_messages/$',views.UnreadMessagesView.as_view(), name='unread_messages'),
     url(r'^user_status/$',views.UserStatusView.as_view(), name='user_status'),
]
