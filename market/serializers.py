from rest_framework import serializers
from .models import Market


class MarketSerializerForSearchByName(serializers.ModelSerializer):
    class Meta:
        model = Market
        fields = ('market_name',)


class MarketSerializerForSearchByAddress(serializers.ModelSerializer):
    class Meta:
        model = Market
        fields = ('address',)


class MarketSerializerForAdd(serializers.ModelSerializer):
    class Meta:
        model = Market
        fields = ('market_name', 'address', 'phone_number', 'description', 'owner',)


class MarketSerializerForUser(serializers.ModelSerializer):
    class Meta:
        model = Market
        fields = ('id', 'owner',)


class MarketSerializerForID(serializers.ModelSerializer):
    class Meta:
        model = Market
        fields = ('id',)
