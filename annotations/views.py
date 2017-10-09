from django.core.exceptions import ObjectDoesNotExist, SuspiciousFileOperation
from rest_framework.decorators import permission_classes
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView,\
    RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST,\
    HTTP_500_INTERNAL_SERVER_ERROR
from LRMS_Thesis.settings import DEBUG
from annotations.models import Annotation, AnnotationRecording
from annotations.serializers import AnnotationSerializer,\
    AnnotationRecordingSerializer
from user.models import Language


class AnnotationsList(ListAPIView):
    """
    Response class to return all annotations or create a new annotation
    """

    queryset = Annotation.objects.all()
    serializer_class = AnnotationSerializer

    @permission_classes((IsAdminUser,))
    def post(self, request):
        """
        create new annotation
        :return: created annotation or error messages.
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

        # get the language code and create annotation
        try:
            language = Language.objects.get(code=request.data['language'])
            text = request.data['text']
            if len(text) < 2:
                data = {
                    'message': 'Annotation is too short',
                }
                return Response(data, status=HTTP_400_BAD_REQUEST)
            annotation = Annotation(text=text, language=language)
            annotation.save()
            serializer = AnnotationSerializer(annotation)
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

    queryset = Annotation.objects.all()
    serializer_class = AnnotationSerializer
    # todo add admin permissions


class AnnotationRecordingView(RetrieveAPIView):
    queryset = AnnotationRecording.objects.all()
    serializer_class = AnnotationRecordingSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        data = {'message': 'annotation field is required.'}

        if not request.POST.__contains__('annotation'):
            return Response(data, status=HTTP_400_BAD_REQUEST)

        if not request.FILES.__contains__('file'):
            data['message'] = 'No file attached.'
            return Response(data, status=HTTP_400_BAD_REQUEST)

        try:
            user = request.user  # todo fix this
            pk = request.POST.get('annotation')
            annotation = Annotation.objects.get(pk=pk)
            file = request.FILES.get('file')
            if len(file.name) < 5:
                # filename too short
                raise SuspiciousFileOperation

            # todo validate file

            recording = AnnotationRecording(
                user=user,
                annotation=annotation,
                file_url=file,
                file_type=file.name[-3:].upper()
            )
            recording.save()
            s = AnnotationRecordingSerializer(recording)
            return Response(s.data, status=HTTP_201_CREATED)

        except SuspiciousFileOperation:
            data['message'] = 'filename too short'
            return Response(data, status=HTTP_400_BAD_REQUEST)

        except Exception as e:
            data['message'] = str(e) if DEBUG else 'Something went wrong.'
            return Response(data, status=HTTP_500_INTERNAL_SERVER_ERROR)
