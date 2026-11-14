from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Any


@dataclass
class User:
    username: str
    email: str
    keycloak_id: str
    roles: list[str]
    created_at: datetime

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "User":
        if isinstance(data["created_at"], str):
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        return cls(**data)


@dataclass
class Session:
    user_id: str
    access_token: str
    expires_at: datetime
    created_at: datetime

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Session":
        if isinstance(data["expires_at"], str):
            data["expires_at"] = datetime.fromisoformat(data["expires_at"])
        if isinstance(data["created_at"], str):
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        return cls(**data)

    def is_expired(self) -> bool:
        return datetime.now() > self.expires_at
