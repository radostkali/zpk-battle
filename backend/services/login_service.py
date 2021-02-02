from werkzeug.security import check_password_hash

from daos import AuthDAO
from exceptions import LoginException
from entities import UserEntity


class LoginService:

    def __init__(self, auth_dao: AuthDAO):
        self.auth_dao = auth_dao

    def execute(self, username: str, password: str) -> UserEntity:
        try:
            user_entity = self.auth_dao.get_user_by_username(username=username)
        except self.auth_dao.UserDoesNotExists:
            raise LoginException(message='Пользователя с таким никнэймом не существует')

        if not check_password_hash(user_entity.password, password):
            raise LoginException(message='Неверный никнэйм или пароль')

        self.auth_dao.login_user(user_id=user_entity.pk)
        return user_entity
