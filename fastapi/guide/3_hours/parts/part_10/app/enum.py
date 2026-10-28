from enum import StrEnum, auto


class CurrencyEnum(StrEnum):
    RUB = auto()  # На выходе "rub"
    USD = auto()
    EUR = auto()


class OperationEnum(StrEnum):
    INCOME = auto()
    EXPANSE = auto()
    TRANSFER = auto()
