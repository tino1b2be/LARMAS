from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now

from user.models import Language


class Frequency(models.Model):
    """
    Model to store the minimum and maximum number
    of recordings for annotations.
    """
    max = models.IntegerField()
    min = models.IntegerField()
    date = models.DateTimeField(default=now)

    def __str__(self):
        return 'min=' + str(self.min) + '; max=' + str(self.max)


class Annotation(models.Model):
    """
    Model for the annotations
    """
    text = models.TextField(blank=False)
    language = models.ForeignKey(Language, blank=False)
    number_of_recordings = models.IntegerField(default=0)
    # todo implement checks

    class Meta:
        # this ordering will affect inserts.
        ordering = ('number_of_recordings',)

    def __str__(self):
        return self.language.name \
               + ' - "' \
               + self.text \
               + '"'


class AnnotationRecording(models.Model):
    """
    Model to store data about the recordings
    """
    recording_url = models.TextField()
    annotation = models.ForeignKey(Annotation)
    quality = models.IntegerField(default=0)
    date = models.DateTimeField(default=now)
    user = models.ForeignKey(User, blank=False)
    # todo implement checks

    def __str__(self):
        # <language_name> - <annotation_text>
        return self.annotation.language.name \
               + ' - "' \
               + self.annotation.text \
               + '"'


class AnnotationTranslation(models.Model):
    """
    Model to store details about translations
    """
    original_annotation = models.ForeignKey(Annotation, blank=False)
    text = models.TextField(blank=False)
    verified = models.BooleanField(default=False)
    language = models.ForeignKey(Language, blank=False)
    user = models.ForeignKey(User, blank=False)
    date = models.DateTimeField(default=now)
    # todo implement checks

    def __str__(self):
        # <old_language> to <new_language>
        return self.original_annotation.language.name \
               + ' to ' \
               + self.language.name
