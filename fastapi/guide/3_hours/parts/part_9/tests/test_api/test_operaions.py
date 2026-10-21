"""AAA - Arrange, Act, Assert"""


from decimal import Decimal
from app.models import User, Wallet


def test_add_expense_success(db_session, client):
    # Arrange - подготовка данных
    user = User(login="test_user_login")
    db_session.add(user)
    db_session.flush()
    wallet = Wallet(name="test_wallet_name", balance=200, user_id=user.id)
    db_session.add(wallet)
    db_session.commit()
    db_session.refresh(wallet)

    # Act - действие
    response = client.post(
        "api/v1/operations/expense",
        json={
            "wallet_name": "test_wallet_name",
            "amount": 50.0,
            "description": "Food"
        },
        headers={"Authorization": f"Bearer {user.login}"}
    )

    # Assert - тест
    assert response.status_code == 200
    assert response.json()["message"] == "Expense added."
    assert response.json()["wallet"] == wallet.name
    assert Decimal(str(response.json()["amount"])) == Decimal(50)
    assert response.json()["description"] == "Food"
    assert Decimal(str(response.json()["balance"])) == Decimal(150)


def test_add_expense_negative_amount(db_session, client):
    user = User(login="test_user_login")
    db_session.add(user)
    db_session.flush()
    wallet = Wallet(name="test_wallet_name", balance=200, user_id=user.id)
    db_session.add(wallet)
    db_session.commit()
    db_session.refresh(wallet)

    response = client.post(
        "api/v1/operations/expense",
        json={
            "wallet_name": "test_user_login",
            "amount": -100.0,
            "description": "Negative amount"
        },
        headers={"Authorization": f"Bearer {user.login}"}
    )

    assert response.status_code == 422


def test_add_expense_wallet_empty_name(db_session, client):
    user = User(login="test_user_login")
    db_session.add(user)
    db_session.flush()
    wallet = Wallet(name="test_wallet_name", balance=200, user_id=user.id)
    db_session.add(wallet)
    db_session.commit()
    db_session.refresh(wallet)

    response = client.post(
        "api/v1/operations/expense",
        json={
            "wallet_name": "   ",  # Пустое имя (strip() - уберёт пробелы)
            "amount": 50.0,
            "description": "Empty name"
        },
        headers={"Authorization": f"Bearer {user.login}"}
    )

    assert response.status_code == 422


def test_add_expense_wallet_not_exists(db_session, client):
    user = User(login="test_user_login")
    db_session.add(user)
    db_session.commit()  # Так как кошелёк не создаём, коммитим после юзера

    response = client.post(
        "api/v1/operations/expense",
        json={
            "wallet_name": "some_name",
            "amount": 50.0,
            "description": "Wallet not exists"
        },
        headers={"Authorization": f"Bearer {user.login}"}
    )

    assert response.status_code == 404  # Статус задан в сервисном слое


def test_add_expense_user_not_authorized(db_session, client):
    user = User(login="test_user_login")
    db_session.add(user)
    db_session.flush()
    wallet = Wallet(name="test_wallet_name", balance=200, user_id=user.id)
    db_session.add(wallet)
    db_session.commit()
    db_session.refresh(wallet)

    response = client.post(
        "api/v1/operations/expense",
        json={
            "wallet_name": "test_wallet_name",
            "amount": 50.0,
            "description": "Not authorized"
        },
        headers={"Authorization": "Bearer unknown_user"}
    )

    assert response.status_code == 401


def test_add_expense_not_enough_money(db_session, client):
    user = User(login="test_user_login")
    db_session.add(user)
    db_session.flush()
    wallet = Wallet(name="test_wallet_name", balance=200, user_id=user.id)
    db_session.add(wallet)
    db_session.commit()
    db_session.refresh(wallet)

    response = client.post(
        "api/v1/operations/expense",
        json={
            "wallet_name": "test_wallet_name",
            "amount": 250.0,
            "description": "Food"
        },
        headers={"Authorization": f"Bearer {user.login}"}
    )

    assert response.status_code == 400  # В сервисном слое задан
