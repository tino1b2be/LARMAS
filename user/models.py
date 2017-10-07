from django.db import models
from django.contrib.auth.models import User


class Language(models.Model):
    """
    Model to store language data
    """
    name = models.CharField(max_length=45)
    code = models.CharField(max_length=10)
    region = models.CharField(max_length=45, blank=True)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    """
    Model to store details about the users
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(null=False)
    first_language = models.ForeignKey(
        Language,
        blank=False,
        related_name='first_language'
    )
    second_language = models.ForeignKey(
        Language,
        blank=False,
        related_name='second_language'
    )
    third_language = models.ForeignKey(
        Language,
        blank=False,
        related_name='third_language'
    )

    def __str__(self):
        return self.user.username
