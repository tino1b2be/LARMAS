from django.contrib import admin

from user.models import UserProfile, Language

admin.site.register(UserProfile)
admin.site.register(Language)
