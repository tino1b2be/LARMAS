from django.conf.urls import url

from prompts.views import PromptsView,\
    PromptDistribution, PromptRejection, PromptDetail

app_name = 'prompts'

urlpatterns = [
    url(
        r'^$',
        PromptsView.as_view(),
        name='prompts'
    ),
    url(
        r'^(?P<pk>\d+)/$',
        PromptDetail.as_view(),
        name='prompt'
    ),
    url(
        r'^retrieve/$',
        PromptDistribution.as_view(),
        name='retrieve'
    ),
    url(
        r'^reject/(?P<pk>\d+)/$',
        PromptRejection.as_view(),
        name='reject'
    ),
]
