from django.contrib import admin
from .models import ExchangeRate, Order, AggregatedOrder, ABANAccount, ConsolidatedOrder

@admin.register(ExchangeRate)
class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = ('currency_name', 'rate', 'updated_at')
    search_fields = ('currency_name',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('currency_name', 'amount', 'user', 'created_at', 'is_processed')
    search_fields = ('currency_name', 'user__username')
    list_filter = ('is_processed', 'currency_name')
    date_hierarchy = 'created_at'

@admin.register(AggregatedOrder)
class AggregatedOrderAdmin(admin.ModelAdmin):
    list_display = ('currency_name', 'total_amount', 'created_at', 'is_processed')
    search_fields = ('currency_name',)
    list_filter = ('is_processed', 'currency_name')
    date_hierarchy = 'created_at'

@admin.register(ABANAccount)
class ABANAccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance')
    search_fields = ('user__username',)

@admin.register(ConsolidatedOrder)
class ConsolidatedOrderAdmin(admin.ModelAdmin):
    list_display = ('currency_name', 'total_amount', 'created_at', 'is_processed')
    search_fields = ('currency_name',)
    list_filter = ('is_processed', 'currency_name')
    date_hierarchy = 'created_at'
