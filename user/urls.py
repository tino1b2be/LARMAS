from django.conf.urls import url

from rest_framework.authtoken import views as auth_views

from user.views import UserRegistration, UserView

app_name = 'user'

urlpatterns = [
    url(
        r'^$',
        UserView.as_view(),
        name='user'
        ),
    url(
        r'^register$',
        UserRegistration.as_view(),
        name='create_user'
    ),
    url(
        r'^api-token-auth/',
        auth_views.obtain_auth_token,
        name='auth_token'
    ),
]
