"""
LRMS_Thesis URL Configuration
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.views.generic import TemplateView

from LARMAS import settings

urlpatterns = [
    url(
        r'^$',
        TemplateView.as_view(template_name='docs/output.html'),
        name='home'
    ),
    url(r'^admin/', admin.site.urls),
    url(r'^v1/prompts/', include('prompts.urls')),
    url(r'^v1/annotations/', include('annotations.urls')),
    url(r'^v1/prompt_translations/', include('translations.urls')),
    url(r'^v1/user/', include('user.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
