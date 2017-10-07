from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import HTTP_403_FORBIDDEN, HTTP_400_BAD_REQUEST


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
        if not request.data.__contains__('first_language'):
            data['message'] = 'first_language field is required'
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
            # todo create corresponding user profile
            # new_profile = UserProfile(
            #
            # )
        except:
            pass

        return Response({}, status=HTTP_403_FORBIDDEN)
