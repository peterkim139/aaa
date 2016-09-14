"""nemo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
import os
from django.http import Http404
from django.views.static import serve

def protected_serve(request,path,document_root=None):
    name = os.path.dirname(settings.BASE_DIR)+request.path
    if os.path.isfile(name):
         return serve(request, path, document_root)
    else:
        raise Http404


urlpatterns = [
     url(r'^', include('accounts.urls', namespace='accounts')),
     url(r'^list/', include('category.urls', namespace='category')),
     url(r'^payment/', include('payment.urls', namespace='payment')),
     url(r'^profile/', include('pages.urls', namespace='profile')),
     url(r'^admin/', include(admin.site.urls)),
     url('', include('social.apps.django_app.urls', namespace='social')),
     url(r'^{}(?P<path>.*)$'.format(settings.MEDIA_URL[1:]), protected_serve, {'document_root': settings.MEDIA_ROOT}),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'accounts.views.error404'
handler500= 'accounts.views.error500'
