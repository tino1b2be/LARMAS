from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import HTTP_403_FORBIDDEN


class User(APIView):
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
        # todo implement
        return Response({}, status=HTTP_403_FORBIDDEN)

    def post(self, request):
        # todo implement
        return Response({}, status=HTTP_403_FORBIDDEN)
