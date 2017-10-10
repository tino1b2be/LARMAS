from django.core.exceptions import ObjectDoesNotExist, SuspiciousFileOperation
from rest_framework.decorators import permission_classes
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView,\
    RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST,\
    HTTP_500_INTERNAL_SERVER_ERROR
from LRMS_Thesis.settings import DEBUG
from annotations.models import Prompt, PromptRecording
from annotations.serializers import PromptSerializer,\
    PromptRecordingSerializer
from user.models import Language


class PromptsList(ListAPIView):
    """
    Response class to return all prompts or create a new prompt
    """

    queryset = Prompt.objects.all()
    serializer_class = PromptSerializer

    @permission_classes((IsAdminUser,))
    def post(self, request):
        """
        create new prompt
        :return: created prompt or error messages.
        """

        # check if fields exist

        if not request.data.__contains__('language'):

            data = {
                        'message': 'language field is required',
                    }
            return Response(data, status=HTTP_400_BAD_REQUEST)

        if not request.data.__contains__('text'):
            data = {
                'message': 'text field is required',
            }
            return Response(data, status=HTTP_400_BAD_REQUEST)

        # get the language code and create prompt
        try:
            language = Language.objects.get(code=request.data['language'])
            text = request.data['text']
            if len(text) < 2:
                data = {
                    'message': 'Prompt is too short',
                }
                return Response(data, status=HTTP_400_BAD_REQUEST)
            prompt = Prompt(text=text, language=language)
            prompt.save()
            serializer = PromptSerializer(prompt)
            return Response(serializer.data, status=HTTP_201_CREATED)
        except ObjectDoesNotExist:
            data = {
                'message': 'That language is not supported.',
            }
            return Response(data, status=HTTP_400_BAD_REQUEST)
        except Exception as e:
            message = str(e) if DEBUG else 'An error has occurred'
            data = {
                'message': message,
            }
            # todo log error
            return Response(data, status=HTTP_500_INTERNAL_SERVER_ERROR)


class AnnotationDetail(RetrieveUpdateDestroyAPIView):

    queryset = Prompt.objects.all()
    serializer_class = PromptSerializer
    # todo add admin permissions


class PromptRecordingView(RetrieveAPIView):
    queryset = PromptRecording.objects.all()
    serializer_class = PromptRecordingSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        data = {'message': 'prompt field is required.'}

        if not request.POST.__contains__('prompt'):
            return Response(data, status=HTTP_400_BAD_REQUEST)

        if not request.FILES.__contains__('file'):
            data['message'] = 'No file attached.'
            return Response(data, status=HTTP_400_BAD_REQUEST)

        try:
            user = request.user  # todo fix this
            pk = request.POST.get('prompt')
            prompt = Prompt.objects.get(pk=pk)
            file = request.FILES.get('file')
            if len(file.name) < 5:
                # filename too short
                raise SuspiciousFileOperation

            # todo validate file

            recording = PromptRecording(
                user=user,
                prompt=prompt,
                file_url=file,
                file_type=file.name[-3:].upper()
            )
            recording.save()
            s = PromptRecordingSerializer(recording)
            return Response(s.data, status=HTTP_201_CREATED)

        except SuspiciousFileOperation:
            data['message'] = 'filename too short'
            return Response(data, status=HTTP_400_BAD_REQUEST)

        except Exception as e:
            data['message'] = str(e) if DEBUG else 'Something went wrong.'
            return Response(data, status=HTTP_500_INTERNAL_SERVER_ERROR)
