from typing import Any, Optional


class LocalDatabase:
    def __init__(self):
        self._data: dict[str, dict[str, Any]] = {
            "users": {},
            "sessions": {},
            "blacklist": {},
        }

    def get(self, table: str, key: str) -> Optional[dict[str, Any]]:
        return self._data.get(table, {}).get(key)

    def set(self, table: str, key: str, value: dict[str, Any]) -> None:
        if table not in self._data:
            self._data[table] = {}
        self._data[table][key] = value

    def delete(self, table: str, key: str) -> bool:
        if table in self._data and key in self._data[table]:
            del self._data[table][key]
            return True
        return False

    def exists(self, table: str, key: str) -> bool:
        return table in self._data and key in self._data[table]

    def get_all(self, table: str) -> dict[str, Any]:
        return self._data.get(table, {}).copy()

    def clear(self) -> None:
        self._data = {"users": {}, "sessions": {}, "blacklist": {}}


db = LocalDatabase()