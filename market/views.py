from rest_framework import generics
from .models import *
from .serializers import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.settings import api_settings
import sys


class MarketAdd(generics.CreateAPIView):
    serializer_class = MarketSerializerForAdd


class MarketFullAdd(generics.CreateAPIView):
    serializer_class = MarketSerializerForFullAdd


class MarketList(generics.ListCreateAPIView):
    queryset = Market.objects.all()
    serializer_class = MarketSerializer


class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductAdd(generics.CreateAPIView):
    serializer_class = ProductSerializer


class RoleList(generics.ListCreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class RoleAdd(generics.CreateAPIView):
    serializer_class = RoleSerializer
