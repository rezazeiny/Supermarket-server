import datetime

from rest_framework import generics
from .models import User
from .serializers import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.settings import api_settings
import sys, random, string, time


def id_generator(size=65, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class UserSignup(generics.CreateAPIView):
    serializer_class = UserSerializerForSignup

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserSignupByUsername(generics.CreateAPIView):
    serializer_class = UserSerializerForSignupUsername

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserLoginByUsername(generics.CreateAPIView):
    # queryset = User.objects.all()
    serializer_class = UserSerializerForLoginByUsername

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        # print(data, file=sys.stderr)
        # request.data
        user = User.objects.filter(user_name=data['user_name'])
        if len(user) == 1 and user[0].password == data['password']:
            del data['user_name']
            del data['password']
            data['api'] = data['csrfmiddlewaretoken']
            user[0].api = data['api']
            user[0].last_login = datetime.datetime.now()
            user[0].api_expire_data = datetime.datetime.now() + datetime.timedelta(days=3)
            del data['csrfmiddlewaretoken']
            data['phone_validation'] = user[0].phone_validation
            data['email_validation'] = user[0].email_validation
            user[0].save()
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(data, status=status.HTTP_404_NOT_FOUND)


class UserLoginByEmail(generics.CreateAPIView):
    # queryset = User.objects.all()
    serializer_class = UserSerializerForLoginByEmail

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        # print(request.data, file=sys.stderr)
        user = User.objects.filter(user_name=data['email'])
        if len(user) == 1 and user[0].password == data['password']:
            del data['email']
            del data['password']
            data['api'] = data['csrfmiddlewaretoken']
            user[0].api = data['api']
            user[0].last_login = datetime.datetime.now()
            user[0].api_expire_data = datetime.datetime.now() + datetime.timedelta(days=3)
            del data['csrfmiddlewaretoken']
            data['phone_validation'] = user[0].phone_validation
            data['email_validation'] = user[0].email_validation
            return Response(data, status=status.HTTP_302_FOUND)
        else:
            return Response(data, status=status.HTTP_404_NOT_FOUND)


class ShowProfileUsername(generics.CreateAPIView):
    # queryset = User.objects.all()
    serializer_class = ShowProfile

    def create(self, request, *args, **kwargs):
        # print(request.data, file=sys.stderr)
        data = request.data.copy()
        user = User.objects.filter(user_name=data['user_name'])
        if len(user) == 1 and user[0].api == data['api']:
            del data['csrfmiddlewaretoken']
            data['email'] = user[0].email
            data['email_validation'] = user[0].email_validation
            data['first_name'] = user[0].first_name
            data['last_name'] = user[0].last_name
            data['phone_number'] = user[0].phone_number
            data['phone_validation'] = user[0].phone_validation
            data['image'] = user[0].image.url
            return Response(data, status=status.HTTP_302_FOUND)
        else:
            return Response(data, status=status.HTTP_404_NOT_FOUND)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = DetailUser


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSummery
