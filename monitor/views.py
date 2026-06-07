from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import CurrencyForm, RegisterForm
from .utils import get_historical_rates, generate_currency_chart
from .models import UserQuery, Currency


def index(request):
    """Главная страница с формой выбора валюты"""
    form = CurrencyForm()
    return render(request, 'monitor/index.html', {'form': form})


def chart_view(request):
    """Страница с графиком курса валюты"""
    chart_data = None
    error_message = None
    form = CurrencyForm(request.GET or None)

    if form.is_valid():
        currency = form.cleaned_data['currency']
        period = int(form.cleaned_data['period'])

        print(f"Выбрана валюта: {currency.code}, период: {period}")

        # Сохраняем запрос пользователя
        if request.user.is_authenticated:
            UserQuery.objects.create(
                user=request.user,
                currency=currency,
                period_days=period
            )
        else:
            UserQuery.objects.create(
                user=None,
                currency=currency,
                period_days=period
            )

        # Получаем данные и строим график
        rates = get_historical_rates(currency.code, period)
        print(f"Получены курсы: {rates}")

        if rates:
            chart_data = generate_currency_chart(rates, currency.code)
            print(f"chart_data получен: {chart_data is not None}")
        else:
            error_message = "Не удалось получить данные о курсе валюты. Попробуйте позже."

    return render(request, 'monitor/chart.html', {
        'form': form,
        'chart_data': chart_data,
        'error_message': error_message,
    })


@login_required
def profile(request):
    """Личный кабинет — история запросов пользователя"""
    user_queries = UserQuery.objects.filter(user=request.user)[:10]
    return render(request, 'monitor/profile.html', {
        'user_queries': user_queries
    })


def register(request):
    """Регистрация нового пользователя"""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('monitor:index')
    else:
        form = RegisterForm()
    return render(request, 'monitor/register.html', {'form': form})