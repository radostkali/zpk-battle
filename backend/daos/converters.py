from entities import RateCategoryEntity, RoundEntity, TrackEntity, RateEntity
from models import RateCategory, Round, Track, Rate


def rate_category_orm_to_entity(rate_category_orm: RateCategory) -> RateCategoryEntity:
    return RateCategoryEntity(
        id=rate_category_orm.id,
        name=rate_category_orm.name,
    )


def round_orm_to_entity(round_category_orm: Round) -> RoundEntity:
    return RoundEntity(
        id=round_category_orm.id,
        number=round_category_orm.number,
        theme=round_category_orm.theme,
        style=round_category_orm.style,
        type=str(round_category_orm.type.value),
        last_day=round_category_orm.last_day,
    )


def track_orm_to_entity(track_orm: Track, user_username: str, user_color: str) -> TrackEntity:
    return TrackEntity(
        id=track_orm.id,
        name=track_orm.name,
        user_id=track_orm.user_id,
        user_username=user_username,
        user_color=user_color,
    )


def rate_orm_to_entity(rate_orm: Rate, user_username: str, user_color: str) -> RateEntity:
    return RateEntity(
        category_id=rate_orm.category_id,
        user_id=rate_orm.user_id,
        track_id=rate_orm.track_id,
        user_username=user_username,
        user_color=user_color,
    )
