import os

from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now

from user.models import Language


class Frequency(models.Model):
    """
    Model to store the minimum and maximum number
    of recordings for prompts.
    """
    max = models.IntegerField()
    min = models.IntegerField()
    date = models.DateTimeField(default=now)

    def __str__(self):
        return 'min=' + str(self.min) + '; max=' + str(self.max)


class Prompt(models.Model):
    """
    Model for the prompts
    """
    text = models.TextField(blank=False)
    language = models.ForeignKey(Language, blank=False)
    number_of_recordings = models.IntegerField(default=0)

    # todo implement checks

    class Meta:
        # ascending order of number of recordings
        ordering = ('number_of_recordings',)

    def __str__(self):
        return self.language.name + ' - "' + self.text + '"'


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
               + ' to ' + self.language.name


class DistributedPrompt(models.Model):
    """
    Model for distributed prompts
    """

    user = models.ForeignKey(User, blank=False)
    prompt = models.ForeignKey(Prompt, blank=False)
    rejected = models.BooleanField(default=False)
    recorded = models.BooleanField(default=False)
    date = models.DateTimeField(default=now)

    def __str__(self):
        return self.user.username + ' - ' + \
               str(self.prompt.id) + ' - ' + \
               str(self.rejected) + ' - ' + \
               str(self.recorded) + ' - ' + \
               str(self.date)
