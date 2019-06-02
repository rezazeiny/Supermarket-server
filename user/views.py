from rest_framework import generics
from .models import User
from .serializers import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.settings import api_settings
import sys


class UserSignupByUsername(generics.CreateAPIView):
    serializer_class = UserSerializerForSignup


class UserLoginByUsername(generics.CreateAPIView):
    # queryset = User.objects.all()
    serializer_class = UserSerializerForLoginByUsername

    def create(self, request, *args, **kwargs):
        # print(request.data, file=sys.stderr)
        user = User.objects.filter(user_name=request.data['user_name'])
        if len(user) == 1 and user[0].password == request.data['password']:
            return Response(request.data, status=status.HTTP_302_FOUND)
        else:
            return Response(request.data, status=status.HTTP_404_NOT_FOUND)


class UserLoginByEmail(generics.CreateAPIView):
    # queryset = User.objects.all()
    serializer_class = UserSerializerForLoginByEmail

    def create(self, request, *args, **kwargs):
        # print(request.data, file=sys.stderr)
        user = User.objects.filter(user_name=request.data['user_name'])
        if len(user) == 1 and user[0].password == request.data['password']:
            return Response(request.data, status=status.HTTP_302_FOUND)
        else:
            return Response(request.data, status=status.HTTP_404_NOT_FOUND)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
