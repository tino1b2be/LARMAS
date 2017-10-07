from django.conf.urls import url

import user.views as views

app_name = 'user'

urlpatterns = [
    url(r'^$', views.User.as_view(), name='this_user_profile'),
    url(r'^register$', views.UserRegistration.as_view(), name='create_user'),
]
