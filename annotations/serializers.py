from rest_framework import serializers
from annotations.models import Annotation, AnnotationRecording, AnnotationTranslation


class AnnotationSerializer(serializers.ModelSerializer):
    """
    Serializer class for the Annotation model
    """
    language = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Annotation
        fields = ('id', 'text', 'language')


class AnnotationRecordingSerializer(serializers.ModelSerializer):
    """
    Serializer class for the AnnotationRecording model
    """
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = AnnotationRecording
        fields = ('user', 'annotation', 'date', 'file_url')


class AnnotationTranslationSerializer(serializers.ModelSerializer):
    """
    Serializer class for the AnnotationTranslation model
    """
    class Meta:
        model = AnnotationTranslation
        fields = '__all__'
