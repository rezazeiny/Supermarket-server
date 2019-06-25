from rest_framework import serializers
from .models import Market, Product, Role


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


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name', 'amount', 'price',)


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ('name', 'role',)
