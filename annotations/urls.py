from django.conf.urls import url
from django.conf.urls.static import static

from LRMS_Thesis import settings
from annotations import views

app_name = 'annotations'

urlpatterns = [
    url(
        r'^$',
        views.AnnotationsList.as_view(),
        name='annotations'
    ),
    url(
        r'^(?P<pk>\d+)/$',
        views.AnnotationDetail.as_view(),
        name='annotation'
    ),
    url(
        r'^upload/',
        views.AnnotationRecordingView.as_view(),
        name='upload_recording'
    )
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
