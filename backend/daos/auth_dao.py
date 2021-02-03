from app import db

from flask_login import login_user

from entities import UserEntity
from models import User


class AuthDAO:

    class UserDoesNotExists(Exception):
        pass
    
    def __init__(self):
        self.db = db

    def _orm_to_entity(self, user_orm: User) -> UserEntity:
        return UserEntity(
            pk=user_orm.id,
            username=user_orm.username,
            password=user_orm.password,
        )

    def get_user_by_username(self, username: str) -> UserEntity:
        user = User.query.filter_by(username=username).first()

        if not user:
            raise self.UserDoesNotExists

        return self._orm_to_entity(user)

    def login_user(self, user_id: int) -> None:
        user = User.query.get(user_id)
        login_user(user, remember=True)
