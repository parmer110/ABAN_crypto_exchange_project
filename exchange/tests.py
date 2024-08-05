from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import ExchangeRate, Order, AggregatedOrder, ABANAccount

class ExchangeRateModelTest(TestCase):
    def setUp(self):
        self.rate = ExchangeRate.objects.create(currency_name="BTC", rate=50000.0)

    def test_exchange_rate_str(self):
        self.assertEqual(str(self.rate), "BTC: 50000.0")

class OrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.order = Order.objects.create(currency_name="BTC", amount=50.0, user=self.user)

    def test_order_str(self):
        self.assertEqual(str(self.order), "50.0 BTC by testuser")

class AggregatedOrderModelTest(TestCase):
    def setUp(self):
        self.aggregated_order = AggregatedOrder.objects.create(currency_name="BTC", total_amount=100.0)

    def test_aggregated_order_str(self):
        self.assertEqual(str(self.aggregated_order), "Aggregated 100.0 BTC")

class OrderAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.rate = ExchangeRate.objects.create(currency_name="BTC", rate=50000.0)
        self.user_account = ABANAccount.objects.create(user=self.user, balance=3000000.0)  # افزودن موجودی به حساب کاربر

    def test_create_order(self):
        response = self.client.post('/api/orders/', {'currency_name': 'BTC', 'amount': 50.0, 'user': self.user.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(Order.objects.get().currency_name, 'BTC')

    def test_aggregate_orders(self):
        Order.objects.create(currency_name="BTC", amount=5.0, user=self.user, is_processed=False)
        Order.objects.create(currency_name="BTC", amount=4.0, user=self.user, is_processed=False)

        response = self.client.post('/api/orders/aggregate_orders/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(AggregatedOrder.objects.count(), 1)
        self.assertEqual(AggregatedOrder.objects.get().total_amount, 9.0)

    def test_buy_from_exchange(self):
        response = self.client.post('/api/orders/buy_from_exchange/', {'currency_name': 'BTC', 'amount': 50.0})
        if response.status_code != status.HTTP_200_OK:
            print("Response content:", response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')

class ExchangeRateAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.rate = ExchangeRate.objects.create(currency_name="BTC", rate=50000.0)

    def test_get_exchange_rates(self):
        response = self.client.get('/api/exchange-rates/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['currency_name'], 'BTC')

    def test_update_exchange_rate(self):
        response = self.client.patch(f'/api/exchange-rates/{self.rate.id}/', {'rate': 60000.0})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.rate.refresh_from_db()
        self.assertEqual(self.rate.rate, 60000.0)
