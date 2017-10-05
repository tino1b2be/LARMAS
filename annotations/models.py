from datetime import datetime

from django.contrib.auth.models import User
from django.db import models

from user.models import Language


class Annotation(models.Model):
    """
    Model for the annotations
    """
    text = models.TextField(blank=False)
    language = models.ForeignKey(Language, blank=False)
    number_of_recordings = models.IntegerField(default=0)
    # todo implement checks

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
    date = models.DateTimeField(default=datetime.now())
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
    # todo implement checks

    def __str__(self):
        # <old_language> to <new_language>
        return self.original_annotation.language.name \
               + ' to ' \
               + self.language.name
