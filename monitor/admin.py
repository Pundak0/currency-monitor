from django.contrib import admin
from .models import Currency, RateHistory, UserQuery

@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    search_fields = ('code', 'name')

@admin.register(RateHistory)
class RateHistoryAdmin(admin.ModelAdmin):
    list_display = ('currency', 'date', 'rate')
    list_filter = ('currency', 'date')
    search_fields = ('currency__code',)

@admin.register(UserQuery)
class UserQueryAdmin(admin.ModelAdmin):
    list_display = ('user', 'currency', 'query_date', 'period_days')
    list_filter = ('currency', 'query_date')
    search_fields = ('user__username', 'currency__code')