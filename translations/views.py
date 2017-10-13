from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAdminUser
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
    pass
