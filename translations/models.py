from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now

from prompts.models import Prompt
from user.models import Language


class PromptTranslation(models.Model):
    """
    Model to store details about translations
    """
    original_prompt = models.ForeignKey(Prompt, blank=False)
    text = models.TextField(blank=False)
    verified = models.BooleanField(default=False)
    language = models.ForeignKey(Language, blank=False)
    user = models.ForeignKey(User, blank=False)
    date = models.DateTimeField(default=now)

    # todo implement checks

    def __str__(self):
        # <old_language> to <new_language>
        return self.original_prompt.language.name \
               + ' to ' + self.language.name \
               + ': ' + self.original_prompt.text \
               + ' -> ' + self.text
