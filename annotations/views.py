from django.core.exceptions import ObjectDoesNotExist
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.status import \
    HTTP_201_CREATED, HTTP_400_BAD_REQUEST,\
    HTTP_500_INTERNAL_SERVER_ERROR
from LRMS_Thesis.settings import DEBUG
from annotations.models import Annotation
from annotations.serializers import AnnotationSerializer
from user.models import Language


class AnnotationsList(ListAPIView):
    """
    Response class to return all annotations or create a new annotation
    """
    # todo only available to admin users
    queryset = Annotation.objects.all()
    serializer_class = AnnotationSerializer
    paginate_by = 5  # todo finish this off

    # todo permission_classes = (IsAdminUser,)

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


class AnnotationDetail(RetrieveAPIView):

    queryset = Annotation.objects.all()
    serializer_class = AnnotationSerializer
