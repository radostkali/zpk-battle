from datetime import date
from dataclasses import dataclass
from typing import Optional


@dataclass
class UserEntity:
    pk: int
    username: str
    password: str


@dataclass
class RateCategoryEntity:
    id: int
    name: str


@dataclass
class RoundEntity:
    id: int
    number: int
    theme: str
    type: str
    last_day: date
    style: Optional[str] = None

    def __hash__(self):
        return hash(self.id)


@dataclass
class TrackEntity:
    id: int
    name: str
    user_id: int
    user_username: str
    user_color: str


@dataclass
class RateEntity:
    category_id: int
    user_id: int
    track_id: int
    user_username: str
    user_color: str
