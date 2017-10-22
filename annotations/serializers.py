from rest_framework import serializers

from annotations.models import PromptRecording


class PromptRecordingSerializer(serializers.ModelSerializer):
    """
    Serializer class for the PromptRecording model
    """
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = PromptRecording
        fields = ('user', 'prompt', 'date', 'file_url', 'annotation')
