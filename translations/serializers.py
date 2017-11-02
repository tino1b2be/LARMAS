from rest_framework import serializers

from translations.models import PromptTranslation


class PromptTranslationSerializer(serializers.ModelSerializer):
    """
    Serializer class for the PromptTranslation model
    """
    original_prompt = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    language = serializers.SlugRelatedField(slug_field='code', read_only=True)

    class Meta:
        model = PromptTranslation
        fields = (
            'id',
            'original_prompt',
            'text',
            'language',
            'verified',
            'date'
        )
