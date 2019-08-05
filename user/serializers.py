from rest_framework import serializers
from .models import User


class DetailUser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'user_name', 'password', 'forgot_password_random', 'email', 'email_validation', 'email_random',
            'first_name', 'last_name',
            'phone_number', 'phone_validation', 'phone_random', 'register_data', 'last_edit_data', 'api',
            'api_expire_data', 'last_login', 'image')


class ProfilePage(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'user_name', 'email', 'email_validation', 'first_name', 'last_name', 'phone_number', 'phone_validation',
            'image', 'api')
        read_only_fields = ('image',)


class ShowProfile(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_name', 'api')


class ChangeProfilePage(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'user_name', 'email', 'first_name', 'last_name', 'phone_number', 'api')


class ProfileSummery(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'user_name', 'email', 'first_name', 'last_name', 'image')


class UserSerializerForSignup(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_name', 'email', 'password',)


class UserSerializerForSignupUsername(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_name', 'password',)


class UserSerializerForLoginByUsername(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_name', 'password',)


class UserSerializerForLoginByEmail(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password',)
