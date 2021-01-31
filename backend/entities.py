import dataclasses


@dataclasses.dataclass
class UserEntity:
    pk: int
    username: str
    password: str
