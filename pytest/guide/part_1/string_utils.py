import requests


def palindrome(s: str) -> bool:
    """Проверка на палиндром."""
    for i in range(len(s) // 2):
        if s[i] != s[-i-1]:
            return False
    return True


def _get_stop_words() -> list[str]:
    """Парсинг стоп-слов с гитхаба."""
    response = requests.get("https://bit.ly/en-stop-words").text
    return [
        x.strip()
        for x in response.split("\n") if not x.startswith("#")
    ]


def remove_stop_words(s: str) -> str:
    """Удаление стоп-слов из строки."""
    stop_words = _get_stop_words()
    return " ".join([x for x in s.split() if x not in stop_words])
