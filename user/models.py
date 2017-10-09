from django.conf.global_settings import AUTH_USER_MODEL
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework.authtoken.models import Token


@receiver(post_save, sender=AUTH_USER_MODEL)
# This function is called triggered whenever
# a new user has been created and saved to the database
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Language(models.Model):
    """
    Model to store language data
    """
    name = models.CharField(max_length=45)
    code = models.CharField(max_length=10, unique=True)
    region = models.CharField(max_length=45, blank=True)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    """
    Model to store details about the users
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(default=0, blank=True)
    first_language = models.ForeignKey(
        Language,
        blank=False,
        related_name='first_language'
    )
    second_language = models.ForeignKey(
        Language,
        null=True,
        blank=True,
        related_name='second_language'
    )
    third_language = models.ForeignKey(
        Language,
        null=True,
        blank=True,
        related_name='third_language'
    )

    def __str__(self):
        return self.user.username + ' - ' + self.first_language.name
