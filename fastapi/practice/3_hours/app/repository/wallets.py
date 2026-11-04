from decimal import Decimal
from sqlalchemy.orm import Session
from app.models import Wallet
from app.enum import CurrencyEnum


def is_wallet_exist(db: Session, user_id: int, wallet_name: str) -> bool:
    # В базе есть хотя бы одна строка для конкретного кошелька
    return db.query(Wallet).filter(Wallet.name == wallet_name,  Wallet.user_id == user_id).first() is not None


def add_income(db: Session, user_id: int, wallet_name: str, amount: Decimal) -> Wallet:
    wallet = db.query(Wallet).filter(Wallet.name == wallet_name, Wallet.user_id == user_id).first()
    wallet.balance += amount
    return wallet


def add_expense(db: Session, user_id: int, wallet_name: str, amount: Decimal) -> Wallet:
    wallet = db.query(Wallet).filter(Wallet.name == wallet_name, Wallet.user_id == user_id).first()
    wallet.balance -= amount
    return wallet


def get_wallet_balance_by_name(db: Session, user_id: int, wallet_name: str) -> Wallet:
    # В базе есть хотя бы одна строка для конкретного кошелька
    return db.query(Wallet).filter(Wallet.name == wallet_name, Wallet.user_id == user_id).first()


def get_all_wallets(db: Session, user_id: int) -> list[Wallet]:
    return db.query(Wallet).filter(Wallet.user_id == user_id).all()


def create_wallet(db: Session, user_id: int, wallet_name: str, amount: Decimal, currency: CurrencyEnum) -> Wallet:
    wallet = Wallet(name=wallet_name, balance=amount, user_id=user_id, currency=currency)
    db.add(wallet)
    db.flush()  # Обновляем базу для id (добавляем id для созданного кошелька)
    return wallet


def get_wallet_by_id(db: Session, user_id: int, wallet_id: int) -> Wallet | None:
    return db.query(Wallet).filter(Wallet.id == wallet_id, Wallet.user_id == user_id).scalar()
