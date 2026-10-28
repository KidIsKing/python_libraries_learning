from decimal import Decimal
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.enum import OperationEnum
from app.schemas import OperationRequest, OperationResponse
from app.models import User
from app.repository import wallets as wallets_repository
from app.repository import operations as operations_repository
from app.service import exchange_service


def add_income(db: Session, current_user: User, operation: OperationRequest) -> OperationResponse:
    if not wallets_repository.is_wallet_exist(db, current_user.id, operation.wallet_name):
        raise HTTPException(
            status_code=404,
            detail=f"Wallet '{operation.wallet_name}' not found."
        )
    wallet = wallets_repository.add_income(db, current_user.id, operation.wallet_name, operation.amount)
    created_operation = operations_repository.create_operation(
        db=db,
        wallet_id=wallet.id,
        type=OperationEnum.INCOME,
        amount=operation.amount,
        currency=wallet.currency,
        category=operation.description
    )
    db.commit()
    return OperationResponse.model_validate(created_operation)


def add_expense(db: Session, current_user: User, operation: OperationRequest) -> OperationResponse:
    if not wallets_repository.is_wallet_exist(db, current_user.id, operation.wallet_name):
        raise HTTPException(
            status_code=404,
            detail=f"Wallet '{operation.wallet_name}' not found."
        )
    wallet = wallets_repository.get_wallet_balance_by_name(db, current_user.id, operation.wallet_name)
    if wallet.balance < operation.amount:
        raise HTTPException(
            status_code=400,
            detail=f"Insufficient funds. Available: {wallet.balance}."
        )
    wallet = wallets_repository.add_expense(db, current_user.id, operation.wallet_name, operation.amount)
    created_operation = operations_repository.create_operation(
            db=db,
            wallet_id=wallet.id,
            type=OperationEnum.EXPANSE,
            amount=operation.amount,
            currency=wallet.currency,
            category=operation.description
        )
    db.commit()
    return OperationResponse.model_validate(created_operation)


def get_operations_list(
    db: Session,
    current_user: User,
    wallet_id: int | None = None,
    date_from: datetime | None = None,
    date_to: datetime | None = None
) -> list[OperationResponse]:
    if wallet_id:
        wallet = wallets_repository.get_wallet_by_id(db, current_user.id, wallet_id)
        if not wallet:
            raise HTTPException(
                status_code=404,
                detail=f"Wallet '{wallet_id}' not found."
            )
        wallets_ids = [wallet.id]
    else:
        wallets = wallets_repository.get_all_wallets(db, current_user.id)
        wallets_ids = [w.id for w in wallets]

    operations = operations_repository.get_operations_list(db, wallets_ids, date_from, date_to)

    # Формируем pydantic-модели
    result = []
    for operation in operations:
        result.append(OperationResponse.model_validate(operation))
    return result


# Чтобы задать await нужно сделать функцию корутиной
async def transfer_between_wallets(
    db: Session,
    user_id: int,
    from_wallet_id: int,
    to_wallet_id: int,
    amount: Decimal
) -> OperationResponse:
    wallet_from = wallets_repository.get_wallet_by_id(db, user_id, from_wallet_id)
    wallet_to = wallets_repository.get_wallet_by_id(db, user_id, to_wallet_id)

    if not wallet_from or not wallet_to:
        raise HTTPException(status_code=404, detail="Wallets not found.")

    if wallet_from.balance < amount:
        raise HTTPException(
            status_code=400,
            detail=f"Not enough money: {wallet_from.balance} {wallet_from.currency}."
        )

    # Определяем курс и сумму перевода
    target_amount = amount  # Сколько придёт получателю
    exchange_rate = Decimal("1")  # По умолчанию валюты одинаковые
    if wallet_from.currency != wallet_to.currency:
        exchange_rate = await exchange_service.get_exchange_rate(wallet_from.currency, wallet_to.currency)
    target_amount = round(amount * exchange_rate, 2)

    wallet_from.balance = round(wallet_from.balance - amount, 2)
    wallet_to.balance = round(wallet_to.balance + target_amount, 2)
    operation = operations_repository.create_operation(
        db=db,
        wallet_id=wallet_from.id,
        type=OperationEnum.TRANSFER,
        amount=target_amount,
        currency=wallet_to.currency,
        category="Перевод"
    )
    db.add(operation)
    db.commit()
    return OperationResponse.model_validate(operation)
