from rest_framework import generics
from market_models.models import *
from user.models import *
from .serializers import *
from rest_framework import status
from rest_framework.response import Response
import sys
import datetime
from django.http import JsonResponse
from django.core import serializers
import json


class MarketAdd(generics.CreateAPIView):
    serializer_class = MarketSerializerForAdd

    def create(self, request, *args, **kwargs):
        print(request.data, file=sys.stderr)
        data = request.data.copy()
        if 'csrfmiddlewaretoken' in data.keys():
            del data['csrfmiddlewaretoken']
        user = User.objects.filter(id=data['owner'])
        if 'api' not in data.keys():
            data = {'error': "Miss API."}
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)
        if len(user) == 1 and user[0].api == data['api']:
            market = Market.objects.create(market_name=data['market_name'], address=data['address'],
                                           phone_number=data['phone_number'], description=data['description'],
                                           owner=user[0])
            market.save()
            del data['api']
            return Response(data, status=status.HTTP_201_CREATED)
        elif len(user) == 1:
            data = {'error': "Invalid API."}
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)
        else:
            data = {'error': "Your user not found."}
            return Response(data, status=status.HTTP_404_NOT_FOUND)


class MarketSearchByName(generics.CreateAPIView):
    # queryset = User.objects.all()
    serializer_class = MarketSerializerForSearchByName

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        print(data, file=sys.stderr)
        markets = Market.objects.filter(market_name__contains=data['market_name'])
        if 'csrfmiddlewaretoken' in data.keys():
            del data['csrfmiddlewaretoken']
        data['markets'] = []

        for i in range(len(markets)):
            market = {
                'id': markets[i].id,
                'market_name': markets[i].market_name,
                'address': markets[i].address,
                'image': markets[i].image.url,
                'rates_result': markets[i].rates_result
            }
            data['markets'].append(market)
            # print(market, file=sys.stderr)
            # print(type(markets), file=sys.stderr)

        return Response(data, status=status.HTTP_201_CREATED)


class MarketSearchByAddress(generics.CreateAPIView):
    # queryset = User.objects.all()
    serializer_class = MarketSerializerForSearchByAddress

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        print(data, file=sys.stderr)
        markets = Market.objects.filter(address__contains=data['address'])
        if 'csrfmiddlewaretoken' in data.keys():
            del data['csrfmiddlewaretoken']
        data['markets'] = []

        for i in range(len(markets)):
            market = {
                'id': markets[i].id,
                'market_name': markets[i].market_name,
                'address': markets[i].address,
                'image': markets[i].image.url,
                'rates_result': markets[i].rates_result
            }
            data['markets'].append(market)
            # print(market, file=sys.stderr)
            # print(type(markets), file=sys.stderr)

        return Response(data, status=status.HTTP_201_CREATED)


class MarketRate(generics.CreateAPIView):
    # queryset = User.objects.all()
    serializer_class = MarketSerializerForUser

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        print(data, file=sys.stderr)
        market = Market.objects.filter(id=data['id'])
        user = User.objects.filter(id=data['owner'])
        if 'csrfmiddlewaretoken' in data.keys():
            del data['csrfmiddlewaretoken']
        if 'api' not in data.keys():
            data = {'error': "Miss API."}
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)
        if len(user) == 1 and user[0].api == data['api'] and len(market) == 1 and 0 <= data['rate'] <= 5:
            if len(market[0].rates.filter(user=user[0])) > 0:
                data = {'error': "You can not rate again."}
                return Response(data, status=status.HTTP_503_SERVICE_UNAVAILABLE)
            market[0].rates.create(user=user[0], star=data['rate'])
            market[0].rates_result = int(
                (market[0].rates_count * market[0].rates_result + data['rate']) / (market[0].rates_count + 1))
            market[0].rates_count += 1
            market[0].save()
            del data['api']
            return Response(data, status=status.HTTP_201_CREATED)
        elif len(user) == 1 and len(market) == 1:
            data = {'error': "Invalid API."}
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)
        elif len(user) == 1 and len(market) == 0:
            data = {'error': "Market Not Fount."}
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        elif len(user) == 0 and len(market) == 1:
            data = {'error': "User Not Found."}
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        elif data['rate'] > 5 or data['rate'] < 0:
            data = {'error': "Rate between 0 and 5."}
            return Response(data, status=status.HTTP_417_EXPECTATION_FAILED)
        else:
            data = {'error': "Error."}
            return Response(data, status=status.HTTP_404_NOT_FOUND)


class MarketShowRates(generics.CreateAPIView):
    # queryset = User.objects.all()
    serializer_class = MarketSerializerForID

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        market = Market.objects.filter(id=data['id'])
        if 'csrfmiddlewaretoken' in data.keys():
            del data['csrfmiddlewaretoken']
        if len(market) == 1:
            rates = market[0].rates.all()
            print(rates, file=sys.stderr)
            data['rates_result'] = market[0].rates_result
            data['rates_count'] = market[0].rates_count
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
            data = {'error': "Market Not Found."}
            return Response(data, status=status.HTTP_404_NOT_FOUND)


class MarketComment(generics.CreateAPIView):
    # queryset = User.objects.all()
    serializer_class = MarketSerializerForUser

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        print(data, file=sys.stderr)
        market = Market.objects.filter(id=data['id'])
        user = User.objects.filter(id=data['owner'])
        if 'csrfmiddlewaretoken' in data.keys():
            del data['csrfmiddlewaretoken']
        if 'api' not in data.keys():
            data = {'error': "Miss API."}
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)
        if len(user) == 1 and user[0].api == data['api'] and len(market) == 1 and len(data['comment']) >= 4:
            if len(market[0].comments.filter(user=user[0])) > 0:
                data = {'error': "You can not comment again."}
                return Response(data, status=status.HTTP_503_SERVICE_UNAVAILABLE)
            market[0].comments.create(user=user[0], comment=data['comment'])
            market[0].comments_count += 1
            market[0].save()
            del data['api']
            return Response(data, status=status.HTTP_201_CREATED)
        elif len(user) == 1 and len(market) == 1:
            data = {'error': "Invalid API."}
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)
        elif len(user) == 1 and len(market) == 0:
            data = {'error': "Market Not Fount."}
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        elif len(user) == 0 and len(market) == 1:
            data = {'error': "User Not Found."}
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        elif len(data['comment']) < 4:
            data = {'error': "Comment can not empty."}
            return Response(data, status=status.HTTP_417_EXPECTATION_FAILED)
        else:
            data = {'error': "Error."}
            return Response(data, status=status.HTTP_404_NOT_FOUND)


class MarketShowComments(generics.CreateAPIView):
    # queryset = User.objects.all()
    serializer_class = MarketSerializerForID

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        print(data, file=sys.stderr)
        market = Market.objects.filter(id=data['id'])
        if 'csrfmiddlewaretoken' in data.keys():
            del data['csrfmiddlewaretoken']
        if len(market) == 1:
            comments = market[0].comments.all()
            data['comments_count'] = market[0].comments_count
            data['comments'] = []

            for i in range(len(comments)):
                comment = {
                    'id': comments[i].user.id,
                    'user_name': comments[i].user.user_name,
                    'comment': comments[i].comment,
                    'date': comments[i].register_data,
                }
                data['comments'].append(comment)
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data = {'error': "Market Not Found."}
            return Response(data, status=status.HTTP_404_NOT_FOUND)


##############################################
# rule
##############################################

class MarketRule(generics.CreateAPIView):
    # queryset = User.objects.all()
    serializer_class = MarketSerializerForUser

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        print(data, file=sys.stderr)
        market = Market.objects.filter(id=data['id'])
        user = User.objects.filter(id=data['owner'])
        if 'csrfmiddlewaretoken' in data.keys():
            del data['csrfmiddlewaretoken']
        if 'api' not in data.keys():
            data = {'error': "Miss API."}
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)
        if len(user) == 1 and user[0].api == data['api'] and len(market) == 1 and len(data['rule']) >= 4:
            if len(market[0].rules.filter(user=user[0])) > 0:
                data = {'error': "You can not add rule again."}
                return Response(data, status=status.HTTP_503_SERVICE_UNAVAILABLE)
            market[0].rules.create(user=user[0], role=data['rule'])
            # market[0].comments_count += 1
            market[0].save()
            del data['api']
            return Response(data, status=status.HTTP_201_CREATED)
        elif len(user) == 1 and len(market) == 1:
            data = {'error': "Invalid API."}
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)
        elif len(user) == 1 and len(market) == 0:
            data = {'error': "Market Not Fount."}
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        elif len(user) == 0 and len(market) == 1:
            data = {'error': "User Not Found."}
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        elif len(data['comment']) < 4:
            data = {'error': "Comment can not empty."}
            return Response(data, status=status.HTTP_417_EXPECTATION_FAILED)
        else:
            data = {'error': "Error."}
            return Response(data, status=status.HTTP_404_NOT_FOUND)


class MarketShowRules(generics.CreateAPIView):
    # queryset = User.objects.all()
    serializer_class = MarketSerializerForID

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        print(data, file=sys.stderr)
        market = Market.objects.filter(id=data['id'])
        if 'csrfmiddlewaretoken' in data.keys():
            del data['csrfmiddlewaretoken']
        if len(market) == 1:
            rules = market[0].rules.all()
            # data['comments_count'] = market[0].comments_count
            data['rules'] = []

            for i in range(len(rules)):
                rule = {
                    'id': rules[i].user.id,
                    'user_name': rules[i].user.user_name,
                    'rule': rules[i].role,
                    'date': rules[i].register_data,
                }
                data['rules'].append(rule)
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data = {'error': "Market Not Found."}
            return Response(data, status=status.HTTP_404_NOT_FOUND)


class MarketShowDetail(generics.CreateAPIView):
    # queryset = User.objects.all()
    serializer_class = MarketSerializerForID

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        print(data, file=sys.stderr)
        market = Market.objects.filter(id=data['id'])
        if 'csrfmiddlewaretoken' in data.keys():
            del data['csrfmiddlewaretoken']
        if len(market) == 1:
            comments = market[0].comments.all()
            rules = market[0].rules.all()
            rates = market[0].rates.all()
            models = Model.objects.filter(market=market[0].id)

            data['market_name'] = market[0].market_name
            data['description'] = market[0].description
            data['address'] = market[0].address
            data['phone_number'] = market[0].phone_number
            data['image'] = market[0].image.url
            data['owner'] = {
                'id': market[0].owner.id,
                'user_name': market[0].owner.user_name,
                'first_name': market[0].owner.first_name,
                'last_name': market[0].owner.last_name,
            }
            data['comments_count'] = market[0].comments_count
            data['comments'] = []
            data['rates_result'] = market[0].rates_result
            data['rates_count'] = market[0].rates_count
            data['rates'] = []
            data['models'] = []
            data['rules'] = []

            for i in range(len(comments)):
                comment = {
                    'id': comments[i].user.id,
                    'user_name': comments[i].user.user_name,
                    'comment': comments[i].comment,
                    'date': comments[i].register_data,
                }
                data['comments'].append(comment)

            for i in range(len(rules)):
                rule = {
                    'id': rules[i].user.id,
                    'user_name': rules[i].user.user_name,
                    'rule': rules[i].role,
                    'date': rules[i].register_data,
                }
                data['rules'].append(rule)

            for i in range(len(rates)):
                rate = {
                    'id': rates[i].user.id,
                    'user_name': rates[i].user.user_name,
                    'start': rates[i].star,
                }
                data['rates'].append(rate)

            for i in range(len(models)):
                model = {
                    'id': models[i].id,
                    'product_name': models[i].product_name,
                    'category': models[i].category,
                    'image': models[i].image.url,
                    'price': models[i].price,
                    'count': models[i].count,
                    'rates_result': models[i].rates_result,
                }
                data['model'].append(model)
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data = {'error': "Market Not Found."}
            return Response(data, status=status.HTTP_404_NOT_FOUND)
