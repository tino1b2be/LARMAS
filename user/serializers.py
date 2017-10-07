from rest_framework import serializers
from user.models import Language, UserProfile


class LanguageSerializer(serializers.ModelSerializer):
    """
    Serializer class for the Language Model
    """

    class Meta:
        model = Language
        fields = ('id', 'name', 'code')


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer class for the User Profile Model
    """

    class Meta:
        model = UserProfile
        fields = '__all__'
