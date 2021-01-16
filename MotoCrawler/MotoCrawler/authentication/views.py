from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.serializers import MotoCrawlerUserSerializer


class MotoCrawlerUserCreate(APIView):
    """
    Registers new User.
    Anyone is allowed to use this view, however view
    only accepts data sent by POST requests.
    :return: New user instance and HTTP_201_CREATED response
    or HTTP_400_BAD_REQUEST when unsuccessful.
    """
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request, format='json'):
        serializer = MotoCrawlerUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HelloWorldView(APIView):
    """
    Simple Test View, displaying a pseudo-dictionary key-value pair 'hello: world'.
    Comes in handy when testing authentication-related issues. Sits under 'hello/' endpoint.
    :return: pseudo-dict{"hello":"world"} & HTTP_200_OK response
    """
    def get(self, request):
        return Response(data={"hello": "world"}, status=status.HTTP_200_OK)
