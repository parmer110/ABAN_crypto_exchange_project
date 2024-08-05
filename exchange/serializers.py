from rest_framework import serializers
from .models import Order, ExchangeRate, AggregatedOrder, ABANAccount, ConsolidatedOrder

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class ExchangeRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeRate
        fields = '__all__'

class AggregatedOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = AggregatedOrder
        fields = '__all__'

class ABANAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = ABANAccount
        fields = '__all__'

class ConsolidatedOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsolidatedOrder
        fields = '__all__'
