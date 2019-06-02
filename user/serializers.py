from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone_number', 'email', 'user_name', 'password',)
        # read_only_fields = ('email')


class UserSerializerForSignup(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_name', 'email', 'password',)


class UserSerializerForLoginByUsername(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_name', 'password',)


class UserSerializerForLoginByEmail(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password',)
