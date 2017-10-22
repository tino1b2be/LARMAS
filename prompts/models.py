from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now

from user.models import Language


class Prompt(models.Model):
    """
    Model for the prompts
    """
    text = models.TextField(blank=False)
    language = models.ForeignKey(Language, blank=False)
    number_of_recordings = models.IntegerField(default=0)

    class Meta:
        # ascending order of number of recordings
        ordering = ('number_of_recordings',)

    def __str__(self):
        return self.language.name + ' - "' + self.text + '"'


class DistributedPrompt(models.Model):
    """
    Model for distributed prompts
    """

    user = models.ForeignKey(User, blank=False)
    prompt = models.ForeignKey(Prompt, blank=False)
    rejected = models.BooleanField(default=False)
    recorded = models.BooleanField(default=False)
    translated = models.BooleanField(default=False)
    date = models.DateTimeField(default=now)

    def __str__(self):
        return self.user.username + ' - ' + \
               str(self.prompt.id) + ' - ' + \
               str(self.rejected) + ' - ' + \
               str(self.recorded) + ' - ' + \
               str(self.date)
