from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import HTTP_403_FORBIDDEN, \
    HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_500_INTERNAL_SERVER_ERROR, \
    HTTP_200_OK

from LARMAS.settings import DEBUG
from user.models import Language, UserProfile
from user.serializers import UserProfileSerializer


class UserView(APIView):
    """
    View class to display or change user details
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
        Show user details
        :param request:
        :return:
        """
        try:
            id = int(request.query_params.get('id', 0))
            if request.user.is_staff:
                try:
                    s = User.objects.get(id=id)
                    user_profile = UserProfile.objects.get(user=s)
                    s = UserProfileSerializer(user_profile)
                    return Response(s.data, status=HTTP_200_OK)
                except ObjectDoesNotExist:
                    data = {'detail': 'User does not exist'}
                    return Response(data, status=HTTP_400_BAD_REQUEST)

            elif (id == 0) or (id == request.user.id):
                user_profile = UserProfile.objects.get(user=request.user)
                s = UserProfileSerializer(user_profile)
                return Response(s.data, status=HTTP_200_OK)
            else:
                return Response(status=HTTP_403_FORBIDDEN)
        except Exception as e:
            data = {'detail': str(e) if DEBUG else 'Something went wrong.'}
            return Response(data, status=HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        """
        View to update user's details
        :param request:
        :return:
        """
        try:
            if request.user.is_staff:
                note = 'Admin users cannot modify their details via API'
                data = {'detail': note}
                return Response(data, status=HTTP_400_BAD_REQUEST)
            d = request.POST
            user = request.user
            user_profile = UserProfile.objects.get(user=user)
            user.email = d.get('email', user.email)
            user.first_name = d.get('first_name', user.first_name)
            user.last_name = d.get('last_name', user.last_name)

            l1 = d.get('first_language', 0)
            l2 = d.get('second_language', 0)
            l3 = d.get('third_language', 0)

            if l1 != 0:
                l11 = Language.objects.get(code=l1)
                user_profile.first_language = l11
            if l2 != 0:
                l22 = Language.objects.get(code=l2)
                user_profile.second_language = l22
            if l3 != 0:
                l33 = Language.objects.get(code=l3)
                user_profile.third_language = l33

            user.save()
            user_profile.save()
            s = UserProfileSerializer(user_profile)
            return Response(s.data, status=HTTP_200_OK)
        except ObjectDoesNotExist:
            data = {'detail': 'Language does not exist.'}
            return Response(data, status=HTTP_400_BAD_REQUEST)
        except Exception as e2:
            data = {'detail': str(e2) if DEBUG else 'Something went wrong'}
            return Response(data, status=HTTP_500_INTERNAL_SERVER_ERROR)


class UserRegistration(APIView):
    """
    View class to register a new user
    """
    permission_classes = (AllowAny,)

    # def get(self, request):
    #     return Response({}, status=HTTP_403_FORBIDDEN)

    def post(self, request):
        data = {'detail': 'username field is required'}

        # check for username field
        if not request.data.__contains__('username'):
            return Response(data, status=HTTP_400_BAD_REQUEST)

        # check if username is unique
        if User.objects.filter(username=request.data['username']).exists():
            data['detail'] = 'That username already exists.'
            return Response(data, status=HTTP_400_BAD_REQUEST)

        # check for password field
        if not request.data.__contains__('password'):
            data['detail'] = 'password field is required'
            return Response(data, status=HTTP_400_BAD_REQUEST)

        # check for first language
        if not request.data.__contains__('first_language'):
            data['detail'] = 'first_language field is required'
            return Response(data, status=HTTP_400_BAD_REQUEST)

        # check if first language is valid
        code = request.data['first_language']
        if not Language.objects.filter(code=code).exists():
            data['detail'] = 'first_language entered does not exist'
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
                first_language=Language.objects.get(code=code),
            )
            try:
                code = request.data.get('second_language', 'X')
                if code == 'X':
                    # second language not entered.
                    new_profile.save()
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
                    s = UserProfileSerializer(new_profile)
                    return Response(s.data, status=HTTP_201_CREATED)

                # third language entered
                third_language = Language.objects.get(code=code)
                new_profile.third_language = third_language
                new_profile.save()
                s = UserProfileSerializer(new_profile)
                return Response(s.data, status=HTTP_201_CREATED)

            except ObjectDoesNotExist:
                new_user.delete()
                data['detail'] = code + ' language code is invalid.'
                return Response(data, status=HTTP_400_BAD_REQUEST)

        except Exception as e2:
            # todo log
            data['detail'] = str(e2) if DEBUG else 'Something went wrong'
            return Response(data, status=HTTP_500_INTERNAL_SERVER_ERROR)
