from rest_framework import serializers
from annotations.models import Annotation


class AnnotationSerializer(serializers.ModelSerializer):
    """
    Serializer class for the Annotation model
    """
    language = serializers.SlugRelatedField(slug_field='name', read_only=True)

    # def create(self, validated_data):
    #     return Annotation.objects.create(**validated_data)
    #
    # def update(self, instance, validated_data):
    #     instance.text = validated_data.get('text', instance.text)
    #     instance.language = validated_data.get('language', instance.language)
    #     instance.save()
    #     return instance

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
