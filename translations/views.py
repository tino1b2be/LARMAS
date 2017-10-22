from django.core.exceptions import ObjectDoesNotExist
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST,\
    HTTP_500_INTERNAL_SERVER_ERROR, HTTP_201_CREATED
from rest_framework.views import APIView

from LARMAS.settings import DEBUG
from prompts.models import DistributedPrompt
from translations.models import PromptTranslation
from translations.serializers import PromptTranslationSerializer
from user.models import Language
from annotations.models import Prompt


class TranslationListView(ListAPIView):
    queryset = PromptTranslation.objects.all()
    serializer_class = PromptTranslationSerializer
    permission_classes = (IsAdminUser,)


class TranslationDetail(RetrieveAPIView):
    queryset = PromptTranslation.objects.all()
    serializer_class = PromptTranslationSerializer
    permission_classes = (IsAdminUser,)


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


class TranslationUploadView(APIView):

    def post(self, request):

        data = {'detail': 'text field is required.'}
        # check if all the relevant data is there
        if not request.POST.__contains__('text'):
            return Response(data, status=HTTP_400_BAD_REQUEST)
        if not request.POST.__contains__('original_prompt'):
            data['detail'] = 'original_prompt field is required.'
            return Response(data, status=HTTP_400_BAD_REQUEST)
        if not request.POST.__contains__('language'):
            data['detail'] = 'language field is required.'
            return Response(data, status=HTTP_400_BAD_REQUEST)

        try:
            user = request.user
            text = request.POST.get('text')
            p = request.POST.get('original_prompt')
            l = request.POST.get('language')
            try:
                prompt = Prompt.objects.get(pk=p)
            except ObjectDoesNotExist:
                data['detail'] = 'The prompt %s does not exist' % p
                return Response(data, status=HTTP_400_BAD_REQUEST)

            try:
                language = Language.objects.get(code=l)
            except ObjectDoesNotExist:
                data['detail'] = 'The language code %s does not exist.' % l
                return Response(data, status=HTTP_400_BAD_REQUEST)

            try:
                d1 = DistributedPrompt.objects.get(prompt=prompt, user=user)
            except ObjectDoesNotExist:
                data['detail'] = 'This prompt was not given to you.'
                return Response(data, status=HTTP_400_BAD_REQUEST)

            translation = PromptTranslation(
                user=user,
                original_prompt=prompt,
                language=language,
                text=text
            )
            d1.translated = True
            d1.save()
            translation.save()
            s = PromptTranslationSerializer(translation)
            return Response(s.data, status=HTTP_201_CREATED)

        except Exception as e:
            data['detail'] = str(e) if DEBUG else 'Something went wrong.'
            return Response(data, status=HTTP_500_INTERNAL_SERVER_ERROR)
