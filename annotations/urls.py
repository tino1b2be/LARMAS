from django.conf.urls import url

from annotations import views

app_name = 'annotations'

urlpatterns = [
    url(
        r'^prompts/$',
        views.PromptsList.as_view(),
        name='prompts'
    ),
    url(
        r'^prompt/(?P<pk>\d+)/$',
        views.PromptDetail.as_view(),
        name='prompt'
    ),
    url(
        r'^upload/$',
        views.PromptRecordingView.as_view(),
        name='upload_recording'
    ),
    url(
        r'^retrieve_prompts/$',
        views.PromptDistribution.as_view(),
        name='distribute_prompts'
    ),
    url(
        r'^reject_prompt/$',
        views.RejectPrompt.as_view(),
        name='reject_prompt'
    )
]
