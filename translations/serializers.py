from rest_framework import serializers

from translations.models import PromptTranslation


class PromptTranslationSerializer(serializers.ModelSerializer):
    """
    Serializer class for the PromptTranslation model
    """
    class Meta:
        model = PromptTranslation
        fields = '__all__'
