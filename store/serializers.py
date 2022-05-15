from abc import ABC

from rest_framework import serializers
from .models import Order, Address
from account.models import User


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class OrderListSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = Order
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id']


class OrderCreateSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)

    class Meta:
        model = Order
        fields = '__all__'

    def get_validation_exclusions(self):
        exlusions = super(OrderCreateSerializer, self).get_validation_exlusions()
        return exlusions+['user']


class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']
