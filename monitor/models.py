from django.db import models
from django.contrib.auth.models import User


class Currency(models.Model):
    """Модель для хранения информации о валюте"""
    code = models.CharField(max_length=3, unique=True, verbose_name="Код валюты")
    name = models.CharField(max_length=50, verbose_name="Название")
    flag_icon = models.CharField(max_length=50, blank=True, null=True, verbose_name="Иконка флага")

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = "Валюта"
        verbose_name_plural = "Валюты"


class RateHistory(models.Model):
    """Модель для хранения исторических курсов валют"""
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='rates', verbose_name="Валюта")
    date = models.DateField(verbose_name="Дата")
    rate = models.DecimalField(max_digits=10, decimal_places=4, verbose_name="Курс к RUB")
    source = models.CharField(max_length=50, default='Frankfurter API', verbose_name="Источник")

    def __str__(self):
        return f"{self.currency.code} на {self.date}: {self.rate} RUB"

    class Meta:
        unique_together = ('currency', 'date')
        verbose_name = "История курса"
        verbose_name_plural = "История курсов"
        ordering = ['-date']


class UserQuery(models.Model):
    """Модель для логирования запросов пользователей"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Пользователь")
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, verbose_name="Валюта")
    query_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата запроса")
    period_days = models.IntegerField(default=7, verbose_name="Период (дни)")

    def __str__(self):
        user_name = self.user.username if self.user else "Гость"
        return f"{user_name} запросил {self.currency.code} за {self.period_days} дней"

    class Meta:
        verbose_name = "Запрос пользователя"
        verbose_name_plural = "Запросы пользователей"
        ordering = ['-query_date']