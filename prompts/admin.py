from django.contrib import admin

from prompts.models import DistributedPrompt, Prompt

admin.site.register(Prompt)
admin.site.register(DistributedPrompt)
