from rest_framework import generics
from market.models import *
from user.models import *
from .serializers import *
from rest_framework import status
from rest_framework.response import Response
import sys
import datetime
from django.http import JsonResponse
from django.core import serializers
import json


class ModelAdd(generics.CreateAPIView):
    serializer_class = ModelSerializerForAdd

    def create(self, request, *args, **kwargs):
        print(request.data, file=sys.stderr)
        data = request.data.copy()
        if 'csrfmiddlewaretoken' in data.keys():
            del data['csrfmiddlewaretoken']
        user = User.objects.filter(id=data['owner'])
        market = Market.objects.filter(id=data['market'])
        if 'api' not in data.keys():
            data = {'error': "Miss API."}
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)
        if len(user) == 1 and len(market) == 1 and user[0].api == data['api']:
            if market[0].owner.id != user[0].id:
                data = {'error': "You are not owner."}
                return Response(data, status=status.HTTP_503_SERVICE_UNAVAILABLE)
            model = Model.objects.create(market=market[0], owner=user[0], product_name=data['product_name'],
                                         description=data['description'], count=data['count'], price=data['price'],
                                         category=data['category'])
            model.save()
            del data['api']
            return Response(data, status=status.HTTP_201_CREATED)
        elif len(user) == 1 and len(market) == 1:
            data = {'error': "Invalid API."}
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)
        else:
            data = {'error': "Your user or market not found."}
            return Response(data, status=status.HTTP_404_NOT_FOUND)


class ModelSearchByName(generics.CreateAPIView):
    # queryset = User.objects.all()
    serializer_class = ModelSerializerForSearchByName

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        print(data, file=sys.stderr)
        all_models = Model.objects.filter(product_name__contains=data['product_name'], market_id=data['market'])
        if 'csrfmiddlewaretoken' in data.keys():
            del data['csrfmiddlewaretoken']
        data['models'] = []

        for i in range(len(all_models)):
            model = {
                'id': all_models[i].id,
                'category': all_models[i].category,
                'product_name': all_models[i].product_name,
                'image': all_models[i].image.url,
                'rates_result': all_models[i].rates_result,
                'price': all_models[i].price,
                'count': all_models[i].count,
            }
            data['models'].append(model)

        return Response(data, status=status.HTTP_201_CREATED)


class ModelSearchByCategory(generics.CreateAPIView):
    # queryset = User.objects.all()
    serializer_class = ModelSerializerForSearchByCategory

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        print(data, file=sys.stderr)
        all_models = Model.objects.filter(category__contains=data['category'], market_id=data['market'])
        if 'csrfmiddlewaretoken' in data.keys():
            del data['csrfmiddlewaretoken']
        data['models'] = []

        for i in range(len(all_models)):
            model = {
                'id': all_models[i].id,
                'category': all_models[i].category,
                'product_name': all_models[i].product_name,
                'image': all_models[i].image.url,
                'rates_result': all_models[i].rates_result,
                'price': all_models[i].price,
                'count': all_models[i].count,
            }
            data['models'].append(model)

        return Response(data, status=status.HTTP_201_CREATED)


class ModelRate(generics.CreateAPIView):
    # queryset = User.objects.all()
    serializer_class = ModelSerializerForUser

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        print(data, file=sys.stderr)
        model = Model.objects.filter(id=data['id'])
        user = User.objects.filter(id=data['owner'])
        if 'csrfmiddlewaretoken' in data.keys():
            del data['csrfmiddlewaretoken']
        if 'api' not in data.keys():
            data = {'error': "Miss API."}
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)
        if len(user) == 1 and user[0].api == data['api'] and len(model) == 1 and 0 <= data['rate'] <= 5:
            if len(model[0].rates.filter(user=user[0])) > 0:
                data = {'error': "You can not rate again."}
                return Response(data, status=status.HTTP_503_SERVICE_UNAVAILABLE)
            model[0].rates.create(user=user[0], star=data['rate'])
            model[0].rates_result = int(
                (model[0].rates_count * model[0].rates_result + data['rate']) / (model[0].rates_count + 1))
            model[0].rates_count += 1
            model[0].save()
            del data['api']
            return Response(data, status=status.HTTP_201_CREATED)
        elif len(user) == 1 and len(model) == 1:
            data = {'error': "Invalid API."}
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)
        elif len(user) == 1 and len(model) == 0:
            data = {'error': "Model Not Fount."}
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        elif len(user) == 0 and len(model) == 1:
            data = {'error': "User Not Found."}
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        elif data['rate'] > 5 or data['rate'] < 0:
            data = {'error': "Rate between 0 and 5."}
            return Response(data, status=status.HTTP_417_EXPECTATION_FAILED)
        else:
            data = {'error': "Error."}
            return Response(data, status=status.HTTP_404_NOT_FOUND)


class ModelShowRates(generics.CreateAPIView):
    # queryset = User.objects.all()
    serializer_class = ModelSerializerForID

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        model = Model.objects.filter(id=data['id'])
        if 'csrfmiddlewaretoken' in data.keys():
            del data['csrfmiddlewaretoken']
        if len(model) == 1:
            rates = model[0].rates.all()
            print(rates, file=sys.stderr)
            data['rates_result'] = model[0].rates_result
            data['rates_count'] = model[0].rates_count
            data['rates'] = []

            for i in range(len(rates)):
                rate = {
                    'id': rates[i].user.id,
                    'user_name': rates[i].user.user_name,
                    'start': rates[i].star,
                }
                data['rates'].append(rate)
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data = {'error': "Model Not Found."}
            return Response(data, status=status.HTTP_404_NOT_FOUND)


class ModelComment(generics.CreateAPIView):
    # queryset = User.objects.all()
    serializer_class = ModelSerializerForUser

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        print(data, file=sys.stderr)
        model = Model.objects.filter(id=data['id'])
        user = User.objects.filter(id=data['owner'])
        if 'csrfmiddlewaretoken' in data.keys():
            del data['csrfmiddlewaretoken']
        if 'api' not in data.keys():
            data = {'error': "Miss API."}
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)
        if len(user) == 1 and user[0].api == data['api'] and len(model) == 1 and len(data['comment']) >= 4:
            if len(model[0].comments.filter(user=user[0])) > 0:
                data = {'error': "You can not comment again."}
                return Response(data, status=status.HTTP_503_SERVICE_UNAVAILABLE)
            model[0].comments.create(user=user[0], comment=data['comment'])
            model[0].comments_count += 1
            model[0].save()
            del data['api']
            return Response(data, status=status.HTTP_201_CREATED)
        elif len(user) == 1 and len(model) == 1:
            data = {'error': "Invalid API."}
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)
        elif len(user) == 1 and len(model) == 0:
            data = {'error': "Model Not Fount."}
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        elif len(user) == 0 and len(model) == 1:
            data = {'error': "User Not Found."}
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        elif len(data['comment']) < 4:
            data = {'error': "Comment can not empty."}
            return Response(data, status=status.HTTP_417_EXPECTATION_FAILED)
        else:
            data = {'error': "Error."}
            return Response(data, status=status.HTTP_404_NOT_FOUND)


class ModelShowComments(generics.CreateAPIView):
    # queryset = User.objects.all()
    serializer_class = ModelSerializerForID

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        print(data, file=sys.stderr)
        model = Model.objects.filter(id=data['id'])
        if 'csrfmiddlewaretoken' in data.keys():
            del data['csrfmiddlewaretoken']
        if len(model) == 1:
            comments = model[0].comments.all()
            data['comments_count'] = model[0].comments_count
            data['comments'] = []

            for i in range(len(comments)):
                comment = {
                    'id': comments[i].user.id,
                    'user_name': comments[i].user.user_name,
                    'comment': comments[i].comment,
                }
                data['comments'].append(comment)
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data = {'error': "Model Not Found."}
            return Response(data, status=status.HTTP_404_NOT_FOUND)


class ModelShowDetail(generics.CreateAPIView):
    # queryset = User.objects.all()
    serializer_class = ModelSerializerForID

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        print(data, file=sys.stderr)
        model = Model.objects.filter(id=data['id'])
        if 'csrfmiddlewaretoken' in data.keys():
            del data['csrfmiddlewaretoken']
        if len(model) == 1:
            comments = model[0].comments.all()
            rates = model[0].rates.all()
            data['market_name'] = model[0].market.market_name
            data['description'] = model[0].description
            data['category'] = model[0].category
            data['price'] = model[0].price
            data['count'] = model[0].count
            data['image'] = model[0].image.url
            data['owner'] = {
                'id': model[0].owner.id,
                'user_name': model[0].owner.user_name,
                'first_name': model[0].owner.first_name,
                'last_name': model[0].owner.last_name,
            }
            data['comments_count'] = model[0].comments_count
            data['comments'] = []
            data['rates_result'] = model[0].rates_result
            data['rates_count'] = model[0].rates_count
            data['rates'] = []

            for i in range(len(comments)):
                comment = {
                    'id': comments[i].user.id,
                    'user_name': comments[i].user.user_name,
                    'comment': comments[i].comment,
                    'date': comments[i].register_data,
                }
                data['comments'].append(comment)

            for i in range(len(rates)):
                rate = {
                    'id': rates[i].user.id,
                    'user_name': rates[i].user.user_name,
                    'start': rates[i].star,
                }
                data['rates'].append(rate)

            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data = {'error': "Model Not Found."}
            return Response(data, status=status.HTTP_404_NOT_FOUND)
