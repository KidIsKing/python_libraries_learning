from typing import Optional
from datetime import datetime
from app.oauth.models import OAuthUser


oauth_users: dict[str, OAuthUser] = {}  # username -> OAuthUser
github_id_to_username: dict[int, str] = {}  # github_id -> username


def create_or_update_oauth_user(github_user_data: dict) -> OAuthUser:
    github_id = github_user_data["id"]
    username = github_user_data["login"]

    existing_username = github_id_to_username.get(github_id)
    if existing_username and existing_username in oauth_users:
        existing_user = oauth_users[existing_username]
        existing_user.display_name = github_user_data.get("name")
        existing_user.email = github_user_data.get("email")
        existing_user.avatar_url = github_user_data.get("avatar_url")
        existing_user.profile_url = github_user_data.get("html_url")
        existing_user.last_login = datetime.now()
        return existing_user

    oauth_user = OAuthUser(
        github_id=github_id,
        username=username,
        display_name=github_user_data.get("name"),
        email=github_user_data.get("email"),
        avatar_url=github_user_data.get("avatar_url"),
        profile_url=github_user_data.get("html_url"),
    )

    oauth_users[username] = oauth_user
    github_id_to_username[github_id] = username

    return oauth_user


def get_oauth_user_by_username(username: str) -> Optional[OAuthUser]:
    return oauth_users.get(username)


def get_oauth_user_by_github_id(github_id: int) -> Optional[OAuthUser]:
    username = github_id_to_username.get(github_id)
    if username:
        return oauth_users.get(username)
    return None


def delete_oauth_user(username: str) -> bool:
    if username in oauth_users:
        user = oauth_users[username]
        del oauth_users[username]
        if user.github_id in github_id_to_username:
            del github_id_to_username[user.github_id]
        return True
    return False


def clear_oauth_users() -> None:
    oauth_users.clear()
    github_id_to_username.clear()
