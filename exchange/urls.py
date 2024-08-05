from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, ExchangeRateViewSet, index

router = DefaultRouter()
router.register(r'orders', OrderViewSet)
router.register(r'exchange-rates', ExchangeRateViewSet)

urlpatterns = [
    path('', index, name='index'),
    path('api/', include(router.urls)),
    path('api/orders/aggregate_orders/', OrderViewSet.as_view({'post': 'aggregate_orders'}), name='aggregate_orders'),
    path('api/orders/buy_from_exchange/', OrderViewSet.as_view({'post': 'buy_from_exchange'}), name='buy_from_exchange'),
]
