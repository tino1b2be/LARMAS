from django.conf.urls import url

from annotations import views

app_name = 'annotations'

urlpatterns = [
    url(
        r'^$',
        views.PromptRecordingDetailView.as_view(),
        name='recording'
    ),
    url(
        r'^upload/$',
        views.PromptUploadView.as_view(),
        name='upload'
    ),
    url(
        r'^list/$',
        views.PromptRecordingsListView.as_view(),
        name='list'
    )
]
