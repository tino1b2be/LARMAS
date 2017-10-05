from django.db import models
from django.contrib.auth.models import User


class Language(models.Model):
    """
    Model to store language data
    """
    name = models.CharField(45)
    region = models.CharField(45, blank=True)


class UserProfile(models.Model):
    """
    Model to store details about the users
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    age = models.IntegerField(null=False)
    first_language = models.ForeignKey(Language, blank=False, null=True)
    second_language = models.ForeignKey(Language, blank=True)
    third_language = models.ForeignKey(Language, blank=True)

