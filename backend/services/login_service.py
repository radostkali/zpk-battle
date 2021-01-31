import dataclasses
from typing import Optional

from werkzeug.security import check_password_hash

from daos import AuthDAO
from entities import UserEntity


class LoginService:
    USER_DOES_NOT_EXISTS = 'Пользователя с таким никнэймом не существует'
    INVALID_PASSWORD = 'Неверный никнэйм или пароль'

    @dataclasses.dataclass
    class LoginResponse:
        user_entity: Optional[UserEntity] = None
        error: Optional[str] = None

    def __init__(self, auth_dao: AuthDAO):
        self.auth_dao = auth_dao

    def execute(self, username: str, password: str) -> LoginResponse:
        try:
            user_entity = self.auth_dao.get_user_by_username(username=username)
        except self.auth_dao.UserDoesNotExists:
            return self.LoginResponse(
                error=self.USER_DOES_NOT_EXISTS,
            )

        if not check_password_hash(user_entity.password, password):
            return self.LoginResponse(
                error=self.INVALID_PASSWORD,
            )

        self.auth_dao.login_user(user_id=user_entity.pk)
        return self.LoginResponse(user_entity=user_entity)
