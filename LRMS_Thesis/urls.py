"""
LRMS_Thesis URL Configuration
"""
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^v1/annotations/', include('annotations.urls')),
    url(r'^v1/user/', include('user.urls')),
]
