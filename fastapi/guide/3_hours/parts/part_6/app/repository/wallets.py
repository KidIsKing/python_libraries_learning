from decimal import Decimal
from sqlalchemy.orm import Session
from models import Wallet


def is_wallet_exist(db: Session, wallet_name: str) -> bool:
    # В базе есть хотя бы одна строка для конкретного кошелька
    return db.query(Wallet).filter(Wallet.name == wallet_name).first() is not None


def add_income(db: Session, wallet_name: str, amount: Decimal) -> Wallet:
    wallet = db.query(Wallet).filter(Wallet.name == wallet_name).first()
    wallet.balance += amount
    return wallet


def add_expense(db: Session, wallet_name: str, amount: Decimal) -> Wallet:
    wallet = db.query(Wallet).filter(Wallet.name == wallet_name).first()
    wallet.balance -= amount
    return wallet


def get_wallet_balance_by_name(db: Session, wallet_name: str) -> Wallet:
    # В базе есть хотя бы одна строка для конкретного кошелька
    return db.query(Wallet).filter(Wallet.name == wallet_name).first()


def get_all_wallets(db: Session) -> list[Wallet]:
    return db.query(Wallet).all()


def create_wallet(db: Session, wallet_name: str, amount: Decimal) -> Wallet:
    wallet = Wallet(name=wallet_name, balance=amount)
    db.add(wallet)
    db.flush()  # Обновляем базу для id
    return wallet
