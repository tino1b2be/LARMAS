from django.conf.urls import url

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
]
