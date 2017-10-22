from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from translations.models import PromptTranslation
from translations.serializers import PromptTranslationSerializer


class TranslationListView(ListAPIView):
    queryset = PromptTranslation.objects.all()
    serializer_class = PromptTranslationSerializer
    permission_classes = (IsAdminUser,)


class TranslationDetail(RetrieveAPIView):
    queryset = PromptTranslation.objects.all()
    serializer_class = PromptTranslationSerializer
    permission_classes = (IsAdminUser,)


class TranslationUploadView(APIView):
    pass


class ParallelView(ListAPIView):
    serializer_class = PromptTranslationSerializer
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        first = self.kwargs.get('first', 0)
        second = self.kwargs.get('second', 0)
        queryset = PromptTranslation.objects.filter(
            language__code=second,
            original_prompt__language__code=first)
        return queryset
