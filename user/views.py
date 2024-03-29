import datetime

from rest_framework import generics
from .models import User
from .serializers import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.settings import api_settings
import sys, random, string, time
from kavenegar import *
import smtplib
from validate_email import validate_email


def send_sms(phone, token):
    print("Sending SMS", file=sys.stderr)
    try:
        api = KavenegarAPI('4F32445549592B37674B394D762B634F7130456D394C5A474255416250487130')
        params = {
            'receptor': phone,
            'template': 'tat',
            'token': token,
            'type': 'sms',  # sms vs call
        }
        response = api.verify_lookup(params)
        print("SMS Sent", file=sys.stderr)
        return response
    except APIException as e:
        print("SMS:", e, file=sys.stderr)
        return e
    except HTTPException as e:
        print("SMS:", e, file=sys.stderr)
        return e


def send_mail(email, msg):
    print("Sending Email", file=sys.stderr)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("rezazeiny1998@gmail.com", "luqscmourqrhprjw")
        server.sendmail(email, email, msg.encode('utf-8').strip())
        server.quit()
        print("Email Sent", file=sys.stderr)
    except Exception as e:
        print("Email:", e, file=sys.stderr)
        return e


def id_generator(size=65, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class UserSignupByUsername(generics.CreateAPIView):
    serializer_class = UserSerializerForSignupUsername

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        print(data, file=sys.stderr)
        if 'csrfmiddlewaretoken' in data.keys():
            token = data['csrfmiddlewaretoken']
            del data['csrfmiddlewaretoken']
        else:
            token = id_generator(64)
        user = User.objects.filter(user_name=data['user_name'])
        if len(user) == 0 and len(data['password']) >= 8 and len(data['user_name']) >= 4:
            user = User.objects.create(user_name=data['user_name'], password=data['password'])
            del data['password']
            data['api'] = token
            data['id'] = user.id
            data['first_name'] = user.first_name
            data['last_name'] = user.last_name
            data['image'] = user.image.url
            data['email'] = user.email
            data['email_validation'] = user.email_validation
            data['phone_number'] = user.phone_number
            data['phone_validation'] = user.phone_validation
            data['image'] = user.image.url
            user.api = data['api']
            user.last_login = datetime.datetime.now()
            user.api_expire_data = datetime.datetime.now() + datetime.timedelta(days=3)
            user.save()
            return Response(data, status=status.HTTP_201_CREATED)
        elif len(user) > 0:
            data['error'] = "Your username is duplicate."
            return Response(data, status=status.HTTP_306_RESERVED)
        elif len(data['password']) < 8:
            data['error'] = "Your password length invalid."
            return Response(data, status=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS)
        elif len(data['user_name']) < 4:
            data['error'] = "Your username length invalid."
            return Response(data, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        else:
            data['error'] = "Etc."
            return Response(data, status=status.HTTP_404_NOT_FOUND)


class UserLoginByUsername(generics.CreateAPIView):
    # queryset = User.objects.all()
    serializer_class = UserSerializerForLoginByUsername

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        print(data, file=sys.stderr)
        if 'csrfmiddlewaretoken' in data.keys():
            token = data['csrfmiddlewaretoken']
            del data['csrfmiddlewaretoken']
        else:
            token = id_generator(64)
        user = User.objects.filter(user_name=data['user_name'])
        if len(user) == 1 and user[0].password == data['password']:
            del data['password']
            data['api'] = token
            data['id'] = user[0].id
            data['first_name'] = user[0].first_name
            data['last_name'] = user[0].last_name
            data['image'] = user[0].image.url
            data['email'] = user[0].email
            data['email_validation'] = user[0].email_validation
            data['phone_number'] = user[0].phone_number
            data['phone_validation'] = user[0].phone_validation
            data['image'] = user[0].image.url
            user[0].api = data['api']
            user[0].last_login = datetime.datetime.now()
            user[0].api_expire_data = datetime.datetime.now() + datetime.timedelta(days=3)
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
        if 'csrfmiddlewaretoken' in data.keys():
            token = data['csrfmiddlewaretoken']
            del data['csrfmiddlewaretoken']
        else:
            token = id_generator(64)
        user = User.objects.filter(user_name=data['email'])
        if len(user) == 1 and user[0].password == data['password']:
            del data['password']
            data['api'] = token
            data['id'] = user[0].id
            data['first_name'] = user[0].first_name
            data['last_name'] = user[0].last_name
            data['image'] = user[0].image.url
            data['user_name'] = user[0].email
            data['email_validation'] = user[0].email_validation
            data['phone_number'] = user[0].phone_number
            data['phone_validation'] = user[0].phone_validation
            data['image'] = user[0].image.url
            user[0].api = data['api']
            user[0].last_login = datetime.datetime.now()
            user[0].api_expire_data = datetime.datetime.now() + datetime.timedelta(days=3)
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(data, status=status.HTTP_404_NOT_FOUND)


class ShowProfileUsername(generics.CreateAPIView):
    # queryset = User.objects.all()
    serializer_class = ShowProfile

    def create(self, request, *args, **kwargs):
        # print(request.data, file=sys.stderr)
        data = request.data.copy()
        if 'csrfmiddlewaretoken' in data.keys():
            del data['csrfmiddlewaretoken']
        if 'api' not in data.keys():
            data = {'error': "Miss API."}
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)
        user = User.objects.filter(user_name=data['user_name'])
        if len(user) == 1 and user[0].api == data['api']:
            data['id'] = user[0].id
            data['email'] = user[0].email
            data['email_validation'] = user[0].email_validation
            data['first_name'] = user[0].first_name
            data['last_name'] = user[0].last_name
            data['phone_number'] = user[0].phone_number
            data['phone_validation'] = user[0].phone_validation
            data['image'] = user[0].image.url
            return Response(data, status=status.HTTP_201_CREATED)
        elif len(user) == 1:
            del data['user_name']
            del data['api']
            data['error'] = "Invalid API"
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)
        else:
            del data['user_name']
            del data['api']
            data['error'] = "Your user not found."
            return Response(data, status=status.HTTP_404_NOT_FOUND)


class ChangeProfilePage(generics.CreateAPIView):
    # queryset = User.objects.all()
    serializer_class = ChangeProfilePage

    def create(self, request, *args, **kwargs):
        print(request.data, file=sys.stderr)
        data = request.data.copy()
        if 'csrfmiddlewaretoken' in data.keys():
            del data['csrfmiddlewaretoken']
        if 'api' not in data.keys():
            data = {'error': "Miss API."}
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)

        user = User.objects.filter(user_name=data['user_name'])
        if len(user) == 1 and user[0].api == data['api']:
            if validate_email(data['email']):
                rand = id_generator(6, string.digits)
                if user[0].email != data['email']:
                    user[0].email_validation = False
                    send_mail(data['email'], rand)
                    user[0].email_random = rand
                elif not user[0].email_validation:
                    send_mail(data['email'], rand)
                    user[0].email_random = rand
            if len(data['phone_number']) == 11:
                rand = id_generator(6, string.digits)
                if user[0].phone_number != data['phone_number']:
                    user[0].phone_validation = False
                    send_sms(data['phone_number'], rand)
                    user[0].phone_random = rand
                elif not user[0].phone_validation:
                    send_sms(data['phone_number'], rand)
                    user[0].phone_random = rand

            data['id'] = user[0].id
            data['email_validation'] = user[0].email_validation
            data['phone_validation'] = user[0].phone_validation
            data['image'] = user[0].image.url
            user[0].email = data['email']
            user[0].first_name = data['first_name']
            user[0].last_name = data['last_name']
            user[0].phone_number = data['phone_number']
            user[0].save()
            return Response(data, status=status.HTTP_201_CREATED)
        elif len(user) == 1:
            data = {'error': "Invalid API."}
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)
        else:
            data = {'error': "Your user not found."}
            return Response(data, status=status.HTTP_404_NOT_FOUND)


class CheckValidatePhone(generics.CreateAPIView):
    # queryset = User.objects.all()
    serializer_class = UserSerializerForCheckValidatePhone

    def create(self, request, *args, **kwargs):
        print(request.data, file=sys.stderr)
        data = request.data.copy()
        if 'csrfmiddlewaretoken' in data.keys():
            del data['csrfmiddlewaretoken']
        if 'api' not in data.keys():
            data = {'error': "Miss API."}
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)

        user = User.objects.filter(user_name=data['user_name'])
        if len(user) == 1 and user[0].api == data['api'] and user[0].phone_random == data['phone_random']:
            del data['api']
            data['phone_validation'] = True
            user[0].phone_validation = True
            user[0].save()
            return Response(data, status=status.HTTP_201_CREATED)
        elif len(user) == 1 and user[0].phone_random != data['phone_random']:
            data = {'error': "Invalid Code."}
            return Response(data, status=status.HTTP_417_EXPECTATION_FAILED)
        elif len(user) == 1:
            data = {'error': "Invalid API."}
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)
        else:
            data = {'error': "Your user not found."}
            return Response(data, status=status.HTTP_404_NOT_FOUND)


class CheckValidateEmail(generics.CreateAPIView):
    serializer_class = UserSerializerForCheckValidateEmail

    def create(self, request, *args, **kwargs):
        print(request.data, file=sys.stderr)
        data = request.data.copy()
        if 'csrfmiddlewaretoken' in data.keys():
            del data['csrfmiddlewaretoken']
        if 'api' not in data.keys():
            data = {'error': "Miss API."}
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)

        user = User.objects.filter(user_name=data['user_name'])
        if len(user) == 1 and user[0].api == data['api'] and user[0].email_random == data['email_random']:
            del data['api']
            data['email_validation'] = True
            user[0].email_validation = True
            user[0].save()
            return Response(data, status=status.HTTP_201_CREATED)
        elif len(user) == 1 and user[0].email_random != data['email_random']:
            data = {'error': "Invalid Code."}
            return Response(data, status=status.HTTP_417_EXPECTATION_FAILED)
        elif len(user) == 1:
            data = {'error': "Invalid API."}
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)
        else:
            data = {'error': "Your user not found."}
            return Response(data, status=status.HTTP_404_NOT_FOUND)


class ForgotPassCheck(generics.CreateAPIView):
    serializer_class = UserSerializerForForgotValidate

    def create(self, request, *args, **kwargs):
        print(request.data, file=sys.stderr)
        data = request.data.copy()
        if 'csrfmiddlewaretoken' in data.keys():
            del data['csrfmiddlewaretoken']
        user = User.objects.filter(user_name=data['user_name'])
        if len(user) == 1 and user[0].forgot_password_random == data['forgot_password_random'] and \
                (user[0].phone_validation or user[0].email_validation):
            data['forgot_password_random'] = True
            user[0].forgot_password_random = "-1"
            user[0].save()
            return Response(data, status=status.HTTP_201_CREATED)
        elif len(user) == 1 and user[0].forgot_password_random != data['forgot_password_random']:
            data = {'error': "Invalid Code."}
            return Response(data, status=status.HTTP_417_EXPECTATION_FAILED)
        elif len(user) == 1 and not user[0].phone_validation and not user[0].email_validation:
            data = {'error': "You have not any activation way."}
            return Response(data, status=status.HTTP_417_EXPECTATION_FAILED)
        elif len(user) == 1:
            data = {'error': "Invalid Error."}
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)
        else:
            data = {'error': "Your user not found."}
            return Response(data, status=status.HTTP_404_NOT_FOUND)


class ForgotPassPhone(generics.CreateAPIView):
    # queryset = User.objects.all()
    serializer_class = UserSerializerForForgot

    def create(self, request, *args, **kwargs):
        # print(request.data, file=sys.stderr)
        data = request.data.copy()
        if 'csrfmiddlewaretoken' in data.keys():
            del data['csrfmiddlewaretoken']
        user = User.objects.filter(user_name=data['user_name'])
        if len(user) == 1 and user[0].phone_validation:
            rand = id_generator(6, string.digits)
            send_sms(user[0].phone_number, rand)
            user[0].forgot_password_random = rand
            user[0].save()
            return Response(data, status=status.HTTP_201_CREATED)
        elif len(user) == 1:
            if len(user[0].phone_number) != 11:
                data = {'error': "Phone number problem."}
                return Response(data, status=status.HTTP_401_UNAUTHORIZED)
            if not user[0].phone_validation:
                data = {'error': "Phone number not valid."}
                return Response(data, status=status.HTTP_401_UNAUTHORIZED)
            data = {'error': "Invalid Error."}
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)
        else:
            del data['user_name']
            data['error'] = "Your user not found."
            return Response(data, status=status.HTTP_404_NOT_FOUND)


class SendSMS(generics.CreateAPIView):
    # queryset = User.objects.all()
    serializer_class = ShowProfile

    def create(self, request, *args, **kwargs):
        # print(request.data, file=sys.stderr)
        data = request.data.copy()
        if 'csrfmiddlewaretoken' in data.keys():
            del data['csrfmiddlewaretoken']
        if 'api' not in data.keys():
            data = {'error': "Miss API."}
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)
        user = User.objects.filter(user_name=data['user_name'])
        if len(user) == 1 and user[0].api == data['api'] and len(user[0].phone_number) == 11 and not user[
            0].phone_validation:
            rand = id_generator(6, string.digits)
            send_sms(user[0].phone_number, rand)
            user[0].phone_random = rand
            user[0].save()
            return Response(data, status=status.HTTP_201_CREATED)
        elif len(user) == 1:
            if len(user[0].phone_number) != 11:
                data = {'error': "Phone number problem."}
                return Response(data, status=status.HTTP_401_UNAUTHORIZED)
            if user[0].phone_validation:
                data = {'error': "Phone number is valid."}
                return Response(data, status=status.HTTP_401_UNAUTHORIZED)
            data = {'error': "Invalid API."}
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)
        else:
            del data['user_name']
            del data['api']
            data['error'] = "Your user not found."
            return Response(data, status=status.HTTP_404_NOT_FOUND)


class ForgotPassEmail(generics.CreateAPIView):
    # queryset = User.objects.all()
    serializer_class = UserSerializerForForgot

    def create(self, request, *args, **kwargs):
        # print(request.data, file=sys.stderr)
        data = request.data.copy()
        if 'csrfmiddlewaretoken' in data.keys():
            del data['csrfmiddlewaretoken']
        user = User.objects.filter(user_name=data['user_name'])
        if len(user) == 1 and user[0].email_validation:
            rand = id_generator(6, string.digits)
            send_mail(user[0].email, rand)
            user[0].forgot_password_random = rand
            user[0].save()
            return Response(data, status=status.HTTP_201_CREATED)
        elif len(user) == 1:
            if not validate_email(user[0].email):
                data = {'error': "Email problem."}
                return Response(data, status=status.HTTP_401_UNAUTHORIZED)
            if not user[0].email_validation:
                data = {'error': "Email is not valid."}
                return Response(data, status=status.HTTP_401_UNAUTHORIZED)
            data = {'error': "Invalid Error."}
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)
        else:
            del data['user_name']
            data['error'] = "Your user not found."
            return Response(data, status=status.HTTP_404_NOT_FOUND)


class SendEmail(generics.CreateAPIView):
    # queryset = User.objects.all()
    serializer_class = ShowProfile

    def create(self, request, *args, **kwargs):
        # print(request.data, file=sys.stderr)
        data = request.data.copy()
        if 'csrfmiddlewaretoken' in data.keys():
            del data['csrfmiddlewaretoken']
        if 'api' not in data.keys():
            data = {'error': "Miss API."}
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)
        user = User.objects.filter(user_name=data['user_name'])
        if len(user) == 1 and user[0].api == data['api'] and validate_email(user[0].email) and not user[
            0].email_validation:
            rand = id_generator(6, string.digits)
            send_mail(user[0].email, rand)
            user[0].email_random = rand
            user[0].save()
            return Response(data, status=status.HTTP_201_CREATED)
        elif len(user) == 1:
            if not validate_email(user[0].email):
                data = {'error': "Email problem."}
                return Response(data, status=status.HTTP_401_UNAUTHORIZED)
            if user[0].email_validation:
                data = {'error': "Email is valid."}
                return Response(data, status=status.HTTP_401_UNAUTHORIZED)
            data = {'error': "Invalid API."}
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)
        else:
            del data['user_name']
            data['error'] = "Your user not found."
            return Response(data, status=status.HTTP_404_NOT_FOUND)


class ForgotPassChange(generics.CreateAPIView):
    # queryset = User.objects.all()
    serializer_class = UserSerializerForForgotPass

    def create(self, request, *args, **kwargs):
        # print(request.data, file=sys.stderr)
        data = request.data.copy()
        if 'csrfmiddlewaretoken' in data.keys():
            del data['csrfmiddlewaretoken']
        user = User.objects.filter(user_name=data['user_name'])
        if len(user) == 1 and len(data['password']) and user[
            0].forgot_password_random == "-1":
            user[0].password = data['password']
            del data['password']
            user[0].forgot_password_random = ""
            user[0].save()
            return Response(data, status=status.HTTP_201_CREATED)
        elif len(data['password']) < 8:
            data = {'error': "Your password length invalid."}
            return Response(data, status=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS)
        else:
            del data['user_name']
            data['error'] = "Your user not found."
            return Response(data, status=status.HTTP_404_NOT_FOUND)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = DetailUser


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSummery
