from app import db
from models import Track, Round, Rate
from entities import RoundEntity

from .converters import round_orm_to_entity


class BattleControlDAO:

    def check_is_track_exists_by_round_and_user_ids(self, round_id: int, user_id: int) -> bool:
        track = Track.query.filter_by(
            round_id=round_id,
            user_id=user_id,
        ).first()
        return bool(track)

    def create_track(self, round_id: int, user_id: int, track_name: str) -> None:
        new_track = Track(
            round_id=round_id,
            user_id=user_id,
            name=track_name,
        )
        db.session.add(new_track)
        db.session.commit()

    def get_round_entity(self, round_id: int) -> RoundEntity:
        round = Round.query.get(round_id)
        return round_orm_to_entity(round)

    def check_if_rate_exists(
            self,
            round_id: int,
            category_id: int,
            track_id: int,
            user_id: int,
    ) -> bool:
        rate = Rate.query.filter_by(
            round_id=round_id,
            category_id=category_id,
            track_id=track_id,
            user_id=user_id,
        ).first()
        return bool(rate)

    def delete_rate_for_category(
            self,
            round_id: int,
            category_id: int,
            user_id: int,
    ):
        Rate.query.filter_by(
            round_id=round_id,
            category_id=category_id,
            user_id=user_id,
        ).delete()

    def create_rate(
            self,
            round_id: int,
            category_id: int,
            track_id: int,
            user_id: int,
    ):
        new_rate = Rate(
            round_id=round_id,
            category_id=category_id,
            track_id=track_id,
            user_id=user_id,
        )
        db.session.add(new_rate)
        db.session.commit()

    def get_tracks_user_id(self, track_id: int):
        track = Track.query.get(track_id)
        return track.user_id
