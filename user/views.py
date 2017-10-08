from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import HTTP_403_FORBIDDEN,\
    HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_500_INTERNAL_SERVER_ERROR

from LRMS_Thesis.settings import DEBUG
from user.models import Language, UserProfile
from user.serializers import UserProfileSerializer


class UserView(APIView):
    """
    View class to display or change user details
    """
    def get(self, request):
        # todo implement
        return Response({}, status=HTTP_403_FORBIDDEN)

    def post(self, request):
        # todo implement
        return Response({}, status=HTTP_403_FORBIDDEN)


class UserRegistration(APIView):
    """
    View class to register a new user
    """

    def get(self, request):
        return Response({}, status=HTTP_403_FORBIDDEN)

    def post(self, request):
        data = {'message': 'username field is required'}

        # check for username field
        if not request.data.__contains__('username'):
            data['message'] = 'username field is required'
            return Response(data, status=HTTP_400_BAD_REQUEST)

        # check if username is unique
        if User.objects.filter(username=request.data['username']).exists():
            data['message'] = 'That username already exists.'
            return Response(data, status=HTTP_400_BAD_REQUEST)

        # check for password field
        if not request.data.__contains__('password'):
            data['message'] = 'password field is required'
            return Response(data, status=HTTP_400_BAD_REQUEST)

        # check for first language
        if not request.data.__contains__('first_language'):
            data['message'] = 'first_language field is required'
            return Response(data, status=HTTP_400_BAD_REQUEST)

        # check if first language is valid
        code = request.data['language']
        if not Language.objects.filter(code=code).exists():
            data['message'] = 'first_language entered does not exist'
            return Response(data, status=HTTP_400_BAD_REQUEST)

        try:
            # create user
            new_user = User(
                username=request.data['username'],
                email=request.data.get('email', ""),
                first_name=request.data.get('first_name', ""),
                last_name=request.data.get('last_name', ""),
            )
            new_user.set_password(request.data['password'])
            new_user.save()

            # create profile
            new_profile = UserProfile(
                user=new_user,
                first_language=code,
            )
            try:
                code = request.data.get('second_language', 'X')
                if code == 'X':
                    # second language not entered.
                    new_profile.save()
                    data['message'] = code + ' language is invalid.'
                    s = UserProfileSerializer(new_profile)
                    return Response(s.data, status=HTTP_201_CREATED)

                # second language entered
                second_language = Language.objects.get(code=code)
                new_profile.second_language = second_language

                # add third language
                code = request.data.get('third_language', 'X')
                if code == 'X':
                    # third language not entered.
                    new_profile.save()
                    data['message'] = code + ' language is invalid.'
                    s = UserProfileSerializer(new_profile)
                    return Response(s.data, status=HTTP_201_CREATED)

                # third language entered
                third_language = Language.objects.get(code=code)
                new_profile.third_language = third_language
                new_profile.save()
                s = UserProfileSerializer(new_profile)
                return Response(s, status=HTTP_201_CREATED)

            except ObjectDoesNotExist:
                new_user.delete()
                data['message'] = 'language is invalid'
                return Response(data, status=HTTP_400_BAD_REQUEST)

            except Exception as e:
                # todo log
                new_user.delete()
                data['message'] = str(e) if DEBUG else 'Something went wrong'
                return Response(data, status=HTTP_400_BAD_REQUEST)

        except Exception as e2:
            # todo log
            data['message'] = str(e2) if DEBUG else 'Something went wrong'
            return Response(data, status=HTTP_500_INTERNAL_SERVER_ERROR)
