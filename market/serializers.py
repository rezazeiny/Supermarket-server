from rest_framework import serializers
from .models import Market


class MarketSerializerForSearch(serializers.ModelSerializer):
    class Meta:
        model = Market
        fields = ('market_name',)


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


