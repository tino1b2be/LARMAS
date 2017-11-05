from django.contrib.auth.models import User
from django.core.exceptions import SuspiciousFileOperation,\
    ObjectDoesNotExist, ValidationError
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, \
    HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.views import APIView

from LARMAS.settings import DEBUG
from LARMAS.util import create_one_time_profile, upload_is_valid
from annotations.models import PromptRecording
from annotations.serializers import \
    PromptRecordingSerializer
from prompts.models import Prompt, DistributedPrompt


class PromptUploadView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        """
        Upload a prompt recording along with the raw audio recording
        :param request: Request object
        :return: 200 if file upload was successful
        """
        data = {'detail': 'prompt field is required.'}
        try:
            # check if all the relevant data is there
            if not request.POST.__contains__('prompt'):
                return Response(data, status=HTTP_400_BAD_REQUEST)
            if not request.POST.__contains__('annotation'):
                data['detail'] = 'annotation field is required.'
                return Response(data, status=HTTP_400_BAD_REQUEST)
            if not request.FILES.__contains__('file'):
                data['detail'] = 'No file attached.'
                return Response(data, status=HTTP_400_BAD_REQUEST)

            # create a random user
            temp_user = User()
            if request.user.is_authenticated:
                user = request.user
            else:
                try:
                    user = create_one_time_profile(
                        post=request.POST, temp_user=temp_user)
                except ObjectDoesNotExist:
                    data['detail'] = 'first_language field is required' \
                                     ' for one time contributors.'
                    return Response(data, status=HTTP_400_BAD_REQUEST)

            pk = request.POST.get('prompt')
            annotation = request.POST.get('annotation')
            try:
                prompt = Prompt.objects.get(pk=pk)
            except ObjectDoesNotExist:
                if not request.user.is_authenticated:
                    temp_user.delete()
                data['detail'] = 'This prompt does not exist.'
                return Response(data, status=HTTP_400_BAD_REQUEST)
            file = request.FILES.get('file')
            if len(file.name) < 5:
                # filename too short
                if not request.user.is_authenticated:
                    temp_user.delete()
                raise SuspiciousFileOperation

            # verify the uploaded file before saving
            try:
                upload_is_valid(file, 'UPLOAD')

            except ValidationError:
                data['detail'] = 'invalid file upload'
                return Response(data, status=HTTP_400_BAD_REQUEST)

            a = PromptRecording.objects.filter(user=user, prompt=prompt)
            if a.count() != 0:
                data['detail'] = 'This prompt was recorded already.'
                return Response(data, status=HTTP_400_BAD_REQUEST)

            recording = PromptRecording(
                user=user,
                prompt=prompt,
                file_url=file,
                file_type=file.name[-3:].upper(),
                annotation=annotation,
            )
            if request.user.is_authenticated:
                try:
                    d1 = DistributedPrompt.objects.get(
                        prompt=prompt,
                        user=user,
                    )
                    d1.recorded = True
                    d1.save()  # save distributed prompt object
                except ObjectDoesNotExist:
                    data['detail'] = 'This prompt was not given to you.'
                    return Response(data, status=HTTP_400_BAD_REQUEST)

            prompt.number_of_recordings += 1
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
    serializer_class = PromptRecordingSerializer
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        code = self.kwargs.get('language', 'x')
        if code != 'x':
            return \
                PromptRecording.objects.filter(prompt__language__code=code)
        else:
            return PromptRecording.objects.all()


class PromptRecordingDetailView(RetrieveAPIView):
    queryset = PromptRecording.objects.all()
    serializer_class = PromptRecordingSerializer
    permission_classes = (IsAdminUser,)
