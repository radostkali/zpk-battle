from dataclasses import dataclass
from typing import Generator

from app import db
from entities import RateCategoryEntity, RoundEntity, TrackEntity, RateEntity, PairEntity
from models import RateCategory, Round, Track, User, Rate, Pair

from .converters import (
    rate_category_orm_to_entity,
    round_orm_to_entity,
    track_orm_to_entity,
    rate_orm_to_entity,
    pair_orm_to_entity,
)


@dataclass
class RoundTracksDTO:
    round: RoundEntity
    tracks: list[TrackEntity]


class BattleDataDAO:

    def fetch_rate_categories(self) -> list[RateCategoryEntity]:
        categories = RateCategory.query.all()
        return list(map(rate_category_orm_to_entity, categories))

    def fetch_rounds(self) -> Generator[RoundEntity, None, None]:
        rounds = Round.query.order_by(Round.number.desc())
        for round in rounds:
            yield round_orm_to_entity(round)

    def fetch_pairs_by_round_id(self, round_id: int) -> Generator[PairEntity, None, None]:
        pairs = Pair.query.filter_by(round_id=round_id)
        for pair in pairs:
            yield pair_orm_to_entity(pair)

    def fetch_tracks_by_round_id(self, round_id: int) -> Generator[TrackEntity, None, None]:
        tracks_users_join = db.session.query(
            Track, User
        ).filter_by(
            round_id=round_id,
        ).join(
            Track.user
        ).all()
        for track, user in tracks_users_join:
            yield track_orm_to_entity(
                track_orm=track,
                user_username=user.username,
                user_color=user.color,
            )

    def fetch_rates_by_round_id(self, round_id: int) -> Generator[RateEntity, None, None]:
        rates_users_join = db.session.query(
            Rate, User,
        ).filter_by(
            round_id=round_id
        ).join(
            Rate.user
        ).all()
        for rate, user in rates_users_join:
            yield rate_orm_to_entity(
                rate_orm=rate,
                user_username=user.username,
                user_color=user.color,
            )

