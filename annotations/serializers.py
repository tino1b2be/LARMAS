from rest_framework import serializers
from annotations.models import Annotation


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
    class Meta:
        model = Annotation
        fields = '__all__'


class AnnotationTranslationSerializer(serializers.ModelSerializer):
    """
    Serializer class for the AnnotationTranslation model
    """
    class Meta:
        model = Annotation
        fields = '__all__'
