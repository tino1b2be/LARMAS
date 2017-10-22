import os

from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now

from prompts.models import Prompt


class PromptRecording(models.Model):
    """
    Model to store data about the recordings
    """

    def update_filename(instance, filename):
        path = 'recordings/'
        fname = instance.user.username \
            + '-' \
            + str(instance.prompt.id) \
            + '-' \
            + str(instance.date) \
            + str(filename[-4:])

        return os.path.join(path, fname)

    file_type = models.CharField(max_length=10, default='UNKNOWN')
    file_url = models.FileField(upload_to=update_filename)
    prompt = models.ForeignKey(Prompt)
    quality = models.IntegerField(default=0)
    date = models.DateTimeField(default=now)
    user = models.ForeignKey(User, blank=False)
    annotation = models.TextField(blank=False)

    def __str__(self):
        # <language_name> - <prompt_text>
        return self.prompt.language.name \
               + ' - "' + self.prompt.text + '"'
