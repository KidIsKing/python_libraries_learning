from decimal import Decimal
import requests
from app.enum import CurrencyEnum


FALLBACK_RATES: dict[tuple[str, str], Decimal] = {
    (CurrencyEnum.USD, CurrencyEnum.RUB): Decimal(str(95.0)),
    (CurrencyEnum.USD, CurrencyEnum.EUR): Decimal(str(0.92)),
    (CurrencyEnum.EUR, CurrencyEnum.RUB): Decimal(str(103.26)),
    (CurrencyEnum.RUB, CurrencyEnum.EUR): Decimal(str(0.0105)),
    (CurrencyEnum.EUR, CurrencyEnum.USD): Decimal(str(1.087)),
    (CurrencyEnum.RUB, CurrencyEnum.USD): Decimal(str(0.0097)),
}


def get_exchange_rate(base: CurrencyEnum, target: CurrencyEnum) -> Decimal:
    """
    Получает курс обмена между двумя валютами

    Args:
        base: Базовая валюта (из которой конвертируем)
        target: Целевая валюта (в которую конвертируем)

    Returns:
        Курс обмена (сколько единиц целевой валюты за одну единицу базовой)
        Если курс не вайден - возвращает 1 (без конвертации)
    """

    url = f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/{base}.json"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # Обработка исключений всех статусов кроме 200
        data = response.json()
        base_map = data.get(base, {})  # По умолчанию берём пустой словарь
        rate = base_map.get(target)

        if rate and isinstance(rate, (int, float)):
            return Decimal(rate)
        raise KeyError("Rate not found.")

    except Exception:
        return FALLBACK_RATES.get((base, target), Decimal(1))
