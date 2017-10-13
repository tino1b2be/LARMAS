from rest_framework import serializers

from prompts.models import Prompt, DistributedPrompt


class PromptSerializer(serializers.ModelSerializer):
    """
    Serializer class for the Prompt model
    """
    language = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Prompt
        fields = ('id', 'text', 'language')


class DistributedPromptSerializer(serializers.ModelSerializer):
    """
    Serializer class for DistributedPrompt
    """
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = DistributedPrompt
        fields = ('user', 'prompt', 'recorded', 'rejected', 'date')
