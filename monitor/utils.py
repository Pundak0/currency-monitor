import requests
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from datetime import datetime, timedelta
from django.utils import timezone


def get_historical_rates(from_currency, days=7):
    """
    Получает курсы валюты from_currency к RUB за последние days дней
    Возвращает словарь {дата: курс}
    """
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=days)

    # Frankfurter API не любит будущие даты, поэтому используем только прошедшие
    url = f"https://api.frankfurter.app/{start_date}..{end_date}?from={from_currency}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        rates = {}
        for date_str, currencies in data.get('rates', {}).items():
            if 'RUB' in currencies:
                rates[date_str] = currencies['RUB']
        return rates
    except Exception as e:
        print(f"Ошибка API: {e}")
        return {}


def generate_currency_chart(rates_dict, currency_code):
    """
    Строит график курса валюты и возвращает base64-строку для вставки в HTML
    """
    if not rates_dict:
        return None

    df = pd.DataFrame(list(rates_dict.items()), columns=['date', 'rate'])
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')

    # Расчёт аналитики
    min_rate = df['rate'].min()
    max_rate = df['rate'].max()
    avg_rate = df['rate'].mean()
    change = df['rate'].iloc[-1] - df['rate'].iloc[0]
    change_percent = (change / df['rate'].iloc[0]) * 100

    # Построение графика
    plt.figure(figsize=(10, 5))
    plt.plot(df['date'], df['rate'], marker='o', linewidth=2, color='#007bff')
    plt.title(f'Курс {currency_code} к RUB', fontsize=14)
    plt.xlabel('Дата', fontsize=12)
    plt.ylabel('Курс (RUB)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)

    # Добавляем аннотации с мин/макс
    min_date = df[df['rate'] == min_rate]['date'].iloc[0]
    max_date = df[df['rate'] == max_rate]['date'].iloc[0]
    plt.annotate(f'Мин: {min_rate:.2f}', xy=(min_date, min_rate), xytext=(10, -20),
                 textcoords='offset points', arrowprops=dict(arrowstyle='->', color='green'))
    plt.annotate(f'Макс: {max_rate:.2f}', xy=(max_date, max_rate), xytext=(10, 10),
                 textcoords='offset points', arrowprops=dict(arrowstyle='->', color='red'))

    # Сохраняем в base64
    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode()
    plt.close()

    return {
        'image': f"data:image/png;base64,{image_base64}",
        'min_rate': min_rate,
        'max_rate': max_rate,
        'avg_rate': avg_rate,
        'change': change,
        'change_percent': change_percent,
        'current_rate': df['rate'].iloc[-1]
    }


def get_current_rate(from_currency):
    """Получает текущий курс валюты к RUB"""
    rates = get_historical_rates(from_currency, days=1)
    if rates:
        return list(rates.values())[-1]
    return None