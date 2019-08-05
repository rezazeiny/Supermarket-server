from rest_framework import serializers
from .models import Model


class ModelSerializerForSearch(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = ('market', 'product_name',)


class ModelSerializerForAdd(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = ('market', 'product_name', 'description', 'owner', 'count', 'price', )


class ModelSerializerForUser(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = ('id', 'owner',)


class ModelSerializerForID(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = ('id',)


