from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum
from django.http import HttpResponse

from .models import Order, ExchangeRate, AggregatedOrder, ABANAccount, ConsolidatedOrder
from .serializers import OrderSerializer, ExchangeRateSerializer, AggregatedOrderSerializer, ABANAccountSerializer, ConsolidatedOrderSerializer

import requests

def index(request):
    return HttpResponse("Welcome to the Crypto Exchange API!")

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def buy_from_exchange(self, request):
        print("Buy from exchange called")
        currency_name = request.data.get('currency_name')
        amount = float(request.data.get('amount', 0))
        user = request.user

        print(f"Currency: {currency_name}, Amount: {amount}, User: {user}")

        # Fetch the exchange rate
        exchange_rate = ExchangeRate.objects.filter(currency_name=currency_name).first()
        if not exchange_rate:
            return Response({'status': 'error', 'message': 'Exchange rate not found.'}, status=status.HTTP_404_NOT_FOUND)

        print(f"Exchange rate: {exchange_rate.rate}")

        # Calculate the cost
        cost = amount * exchange_rate.rate
        print(f"Cost: {cost}")

        # Check user balance
        user_account = ABANAccount.objects.get(user=user)
        print(f"User account balance before deduction: {user_account.balance}")

        if user_account.balance < cost:
            print("Insufficient balance")
            return Response({'status': 'error', 'message': 'Insufficient balance.'}, status=status.HTTP_400_BAD_REQUEST)

        # Deduct the cost from user account
        user_account.balance -= cost
        user_account.save()

        print(f"User account balance after deduction: {user_account.balance}")

        # Create the order
        order = Order.objects.create(currency_name=currency_name, amount=amount, user=user)
        print(f"Order created with ID: {order.id}")

        # Process the order
        if cost < 10:
            # Add to aggregated order if less than $10
            aggregated_order, created = AggregatedOrder.objects.get_or_create(currency_name=currency_name, is_processed=False)
            aggregated_order.total_amount += amount
            aggregated_order.save()
            aggregated_order.orders.add(order)
            print(f"Added to aggregated order: {aggregated_order.id}")
        else:
            # Process directly with exchange if $10 or more
            response = self._process_with_exchange(currency_name, amount)
            if response.status_code != 200:
                return Response({'status': 'error', 'message': response.text}, status=response.status_code)
            
            order.is_processed = True
            order.save()
            print(f"Order processed directly with exchange: {order.id}")

        return Response({'status': 'success', 'order_id': order.id}, status=status.HTTP_200_OK)

    def _process_with_exchange(self, currency_name, amount):
        # Simulated method to simulate exchange processing
        return Response({'status': 'success'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def aggregate_orders(self, request):
        print("Aggregate orders called")
        # Aggregate all orders with total cost less than $10
        orders_to_aggregate = Order.objects.filter(is_processed=False).annotate(total_cost=Sum('amount')).filter(total_cost__lt=10)

        for order in orders_to_aggregate:
            aggregated_order, created = AggregatedOrder.objects.get_or_create(currency_name=order.currency_name, is_processed=False)
            aggregated_order.total_amount += order.amount
            aggregated_order.save()
            aggregated_order.orders.add(order)
            order.is_processed = True
            order.save()

        return Response({'status': 'success'}, status=status.HTTP_200_OK)

class ExchangeRateViewSet(viewsets.ModelViewSet):
    queryset = ExchangeRate.objects.all()
    serializer_class = ExchangeRateSerializer

class AggregatedOrderViewSet(viewsets.ModelViewSet):
    queryset = AggregatedOrder.objects.all()
    serializer_class = AggregatedOrderSerializer

class ABANAccountViewSet(viewsets.ModelViewSet):
    queryset = ABANAccount.objects.all()
    serializer_class = ABANAccountSerializer

class ConsolidatedOrderViewSet(viewsets.ModelViewSet):
    queryset = ConsolidatedOrder.objects.all()
    serializer_class = ConsolidatedOrderSerializer
