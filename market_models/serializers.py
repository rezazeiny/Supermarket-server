from rest_framework import serializers
from .models import Model


class ModelSerializerForSearchByName(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = ('market', 'product_name',)


class ModelSerializerForSearchByCategory(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = ('market', 'category',)


class ModelSerializerForAdd(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = ('market', 'category', 'product_name', 'description', 'owner', 'count', 'price',)


class ModelSerializerForUser(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = ('id', 'owner',)


class ModelSerializerForID(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = ('id',)
