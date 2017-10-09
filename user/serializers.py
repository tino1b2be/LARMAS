from django.contrib.auth.models import User
from rest_framework import serializers
from user.models import Language, UserProfile


class LanguageSerializer(serializers.ModelSerializer):
    """
    Serializer class for the Language Model
    """

    class Meta:
        model = Language
        fields = ('id', 'name', 'code')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer class for the User Profile Model
    """

    user = UserSerializer()
    first_language = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True)
    second_language = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True)
    third_language = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True)

    class Meta:
        model = UserProfile
        fields = '__all__'
