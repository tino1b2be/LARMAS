from django.conf.urls import url

from translations import views

app_name = 'translation'

urlpatterns = [
    url(
        r'^$',
        views.TranslationDetail.as_view(),
        name='translation'
    ),
    url(
        r'upload/^$',
        views.TranslationUploadView.as_view(),
        name='translation'
    ),
    url(
        r'list/^$',
        views.TranslationListView.as_view(),
        name='translation'
    ),
    url(
        # /parallel/<first_language>-<second_language>/
        r'parallel/(?P<first_language>\w+)-(?P<second_language>\w+)^$',
        views.ParallelView.as_view(),
        name='translation'
    ),
]
