from rest_framework import serializers
from annotations.models import Prompt, PromptRecording, \
    PromptTranslation, DistributedPrompt


class PromptSerializer(serializers.ModelSerializer):
    """
    Serializer class for the Prompt model
    """
    language = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Prompt
        fields = ('id', 'text', 'language')


class PromptRecordingSerializer(serializers.ModelSerializer):
    """
    Serializer class for the PromptRecording model
    """
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = PromptRecording
        fields = ('user', 'prompt', 'date', 'file_url')


class PromptTranslationSerializer(serializers.ModelSerializer):
    """
    Serializer class for the PromptTranslation model
    """
    class Meta:
        model = PromptTranslation
        fields = '__all__'


class DistributedPromptSerializer(serializers.ModelSerializer):
    """
    Serializer class for DistributedPrompt
    """
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = DistributedPrompt
        fields = ('user', 'prompt', 'recorded', 'rejected', 'date')
