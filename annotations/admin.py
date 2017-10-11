from django.contrib import admin

from annotations.models import \
    Prompt, PromptRecording, PromptTranslation

admin.site.register(Prompt)
admin.site.register(PromptRecording)
admin.site.register(PromptTranslation)
