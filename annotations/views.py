from django.core.exceptions import SuspiciousFileOperation, ObjectDoesNotExist
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, \
    HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.views import APIView

from LARMAS.settings import DEBUG
from annotations.models import PromptRecording
from prompts.models import Prompt, DistributedPrompt
from annotations.serializers import \
    PromptRecordingSerializer


class PromptUploadView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        data = {'detail': 'prompt field is required.'}
        # check if all the relevant data is there
        if not request.POST.__contains__('prompt'):
            return Response(data, status=HTTP_400_BAD_REQUEST)
        if not request.POST.__contains__('annotation'):
            data['detail'] = 'annotation field is required.'
            return Response(data, status=HTTP_400_BAD_REQUEST)
        if not request.FILES.__contains__('file'):
            data['detail'] = 'No file attached.'
            return Response(data, status=HTTP_400_BAD_REQUEST)

        try:
            user = request.user  # todo fix this
            pk = request.POST.get('prompt')
            annotation = request.POST.get('annotation')
            try:
                prompt = Prompt.objects.get(pk=pk)
            except ObjectDoesNotExist:
                data['detail'] = 'This prompt does not exist.'
                return Response(data, status=HTTP_400_BAD_REQUEST)
            file = request.FILES.get('file')
            if len(file.name) < 5:
                # filename too short
                raise SuspiciousFileOperation

            # todo validate file

            recording = PromptRecording(
                user=user,
                prompt=prompt,
                file_url=file,
                file_type=file.name[-3:].upper(),
                annotation=annotation,
            )
            try:
                d1 = DistributedPrompt.objects.get(prompt=prompt, user=user)
            except ObjectDoesNotExist:
                data['detail'] = 'This prompt was not given to you.'
                return Response(data, status=HTTP_400_BAD_REQUEST)

            prompt.number_of_recordings += 1
            d1.recorded = True
            d1.save()  # save distributed prompt object
            prompt.save()  # save prompt object
            recording.save()  # save recording
            s = PromptRecordingSerializer(recording)
            return Response(s.data, status=HTTP_201_CREATED)

        except SuspiciousFileOperation:
            data['detail'] = 'filename too short'
            return Response(data, status=HTTP_400_BAD_REQUEST)

        except Exception as e:
            data['detail'] = str(e) if DEBUG else 'Something went wrong.'
            return Response(data, status=HTTP_500_INTERNAL_SERVER_ERROR)


class PromptRecordingsListView(ListAPIView):
    queryset = PromptRecording.objects.all()
    serializer_class = PromptRecordingSerializer
    permission_classes = (IsAdminUser,)


class PromptRecordingDetailView(RetrieveAPIView):
    queryset = PromptRecording.objects.all()
    serializer_class = PromptRecordingSerializer
    permission_classes = (IsAdminUser,)
