import dataclasses
from typing import Optional

from werkzeug.security import check_password_hash

from daos import AuthDAO


class LoginService:
    USER_DOES_NOT_EXISTS = 'Пользователя с таким никнэймом не существует'
    INVALID_PASSWORD = 'Неверный никнэйм или пароль'

    @dataclasses.dataclass
    class LoginResponse:
        is_logged_in: bool
        error: Optional[str] = None

    def __init__(self, auth_dao: AuthDAO):
        self.auth_dao = auth_dao

    def execute(self, username: str, password: str) -> LoginResponse:
        try:
            user = self.auth_dao.get_user_by_username(username=username)
        except self.auth_dao.UserDoesNotExists:
            return self.LoginResponse(
                is_logged_in=False,
                error=self.USER_DOES_NOT_EXISTS,
            )

        if not check_password_hash(user.password, password):
            return self.LoginResponse(
                is_logged_in=False,
                error=self.INVALID_PASSWORD,
            )

        self.auth_dao.login_user(user_id=user.pk)
        return self.LoginResponse(is_logged_in=True)
