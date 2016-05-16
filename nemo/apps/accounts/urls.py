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



from django.conf.urls import patterns,include, url
from django.contrib import admin
from . import views

urlpatterns = [
     url(r'^$',views.HomeView.as_view(),name='account'),
     url(r'^registration/$',views.RegisterView.as_view(),name='registr'),
     url(r'^reset/$',views.ResetView.as_view(),name='reset'),
     url(r'^change_password/(?P<reset_key>\w+)/',views.ChangePasswordView.as_view(),name='change_password'),
     url(r'^login/$',views.LoginView.as_view(),name='login'),
     url(r'^search_results/$',views.SearchView.as_view(),name='search_results'),
     url(r'^profile/$',views.ProfileView.as_view(),name='profile'),
     url(r'^edit_profile/$',views.EditProfileView.as_view(),name='edit_profile'),
     url(r'^logout/$',views.LogoutView.as_view(),name='logout'),
]
