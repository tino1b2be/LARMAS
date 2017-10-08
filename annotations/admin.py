from django.contrib import admin

from annotations.models import \
    Annotation, AnnotationRecording, AnnotationTranslation

admin.site.register(Annotation)
admin.site.register(AnnotationRecording)
admin.site.register(AnnotationTranslation)
