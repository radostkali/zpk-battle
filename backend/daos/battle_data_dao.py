from dataclasses import dataclass
from collections import defaultdict

from app import db
from entities import RateCategoryEntity, RoundEntity, TrackEntity, RateEntity
from models import RateCategory, Round, Track, User, Rate

from .converters import (
    rate_category_orm_to_entity,
    round_orm_to_entity,
    track_orm_to_entity,
    rate_orm_to_entity,
)


@dataclass
class RoundTracksDTO:
    round: RoundEntity
    tracks: list[TrackEntity]


class BattleDataDAO:

    def fetch_rate_categories(self) -> list[RateCategoryEntity]:
        categories = RateCategory.query.all()
        return list(map(rate_category_orm_to_entity, categories))

    def fetch_rounds_with_tracks(self) -> list[RoundTracksDTO]:
        rounds = Round.query.order_by(Round.number.desc())
        round_tracks_dtos = []
        for round in rounds:
            tracks_users_join = db.session.query(
                Track, User,
            ).filter_by(
                round_id=round.id
            ).join(
                Track.user
            ).all()
            tracks_entities = []
            for track, user in tracks_users_join:
                tracks_entities.append(track_orm_to_entity(
                    track_orm=track,
                    user_username=user.username,
                    user_color=user.color,
                ))
            round_track_dto = RoundTracksDTO(
                round=round_orm_to_entity(round),
                tracks=tracks_entities,
            )
            round_tracks_dtos.append(round_track_dto)
        return round_tracks_dtos

    def fetch_rates(self, round_id: int) -> list[RateEntity]:
        rates_users_join = db.session.query(
            Rate, User,
        ).filter_by(
            round_id=round_id
        ).join(
            Rate.user
        ).all()
        rates_entities = []
        for rate, user in rates_users_join:
            rates_entities.append(rate_orm_to_entity(
                rate_orm=rate,
                user_username=user.username,
                user_color=user.color,
            ))
        return rates_entities

