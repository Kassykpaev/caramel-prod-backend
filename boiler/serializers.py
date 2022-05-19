from rest_framework import serializers
from .models import Boiler
from store.serializers import OrderListSerializer


class BoilerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boiler
        fields = '__all__'


class BoilerModeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boiler
        fields = [
            'mode'
        ]


class BoilerAddOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boiler
        fields = [
            'order',
            'initial_order_volume',
            'engine_voltage',
            'engine_target_voltage',
            'coef_i',
            'coef_mv_bar'
        ]


class BoilerUpdateOrderProgress(serializers.ModelSerializer):
    class Meta:
        model = Boiler
        fields = [
            'engine_voltage'
        ]


class BoilerRetrieveSerializer(serializers.ModelSerializer):
    order = OrderListSerializer()

    class Meta:
        model = Boiler
        fields = '__all__'


class BoilerUpdateStatus(serializers.ModelSerializer):
    class Meta:
        model = Boiler
        fields = [
            'id',
            'status'
        ]
