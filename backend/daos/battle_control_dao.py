from app import db
from models import Track, Round, Rate, Pair
from entities import RoundEntity, PairEntity

from sqlalchemy import or_

from .converters import round_orm_to_entity, pair_orm_to_entity


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
        return True if rate else False

    def get_pair_entity(
            self,
            round_id: int,
            track_id: int,
    ) -> PairEntity:
        track = Track.query.get(track_id)
        pair = Pair.query.filter_by(
            round_id=round_id,
        ).filter(
            or_(
                Pair.user_one_id == track.user_id,
                Pair.user_two_id == track.user_id,
                Pair.user_three_id == track.user_id,
            )
        ).first()
        return pair_orm_to_entity(pair)

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
        ).delete(synchronize_session='fetch')
        db.session.commit()

    def delete_rate_for_pair_and_category(
            self,
            round_id: int,
            category_id: int,
            user_id: int,
            pair_entity: PairEntity
    ):
        tracks = Track.query.filter_by(
            round_id=round_id,
        ).filter(
            or_(
                Track.user_id == pair_entity.user_one_id,
                Track.user_id == pair_entity.user_two_id,
                Track.user_id == pair_entity.user_three_id,
            )
        )
        Rate.query.filter_by(
            round_id=round_id,
            category_id=category_id,
            user_id=user_id,
        ).filter(
            Rate.track_id.in_([track.id for track in tracks])
        ).delete(synchronize_session='fetch')
        db.session.commit()

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

    def get_track_user_id(self, track_id: int) -> int:
        track = Track.query.get(track_id)
        return track.user_id

    def check_if_pair_exists(self, round_id: int, user_id: int) -> bool:
        pair = Pair.query.filter_by(
            round_id=round_id,
        ).filter(
            or_(
                Pair.user_one_id == user_id,
                Pair.user_two_id == user_id,
                Pair.user_three_id == user_id,
            )
        ).first()
        return True if pair else False
