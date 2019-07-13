from rest_framework import serializers
from .models import Market


class MarketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Market
        fields = ('name', 'address', 'phone_number', 'owner',)


class MarketSerializerForAdd(serializers.ModelSerializer):
    class Meta:
        model = Market
        fields = ('name', 'owner',)


class MarketSerializerForFullAdd(serializers.ModelSerializer):
    class Meta:
        model = Market
        fields = ('name', 'address', 'phone_number', 'owner',)
