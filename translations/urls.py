from django.conf.urls import url

from translations import views

app_name = 'translations'

urlpatterns = [
    url(
        r'^$',
        views.TranslationListView.as_view(),
        name='translations'
    ),
    url(
        r'^(?P<pk>\d+)/$',
        views.TranslationDetail.as_view(),
        name='translation'
    ),
    url(
        r'^upload/$',
        views.TranslationUploadView.as_view(),
        name='upload'
    ),
    url(
        # /parallel/<first_language>/<second_language>/
        r'^parallel/(?P<first>.+)/(?P<second>.+)/$',
        views.ParallelView.as_view(),
        name='parallel'
    ),
]
