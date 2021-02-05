from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from typing import Optional

from entities import RateCategoryEntity
from daos import BattleDataDAO


@dataclass
class RateDTO:
    categoryId: int
    userId: int
    userUsername: str
    userColor: str


@dataclass
class TrackWithRatesDTO:
    id: int
    name: str
    userId: int
    userUsername: str
    userColor: str
    rates: []


@dataclass
class RoundWithTracksDTO:
    id: int
    number: int
    theme: str
    type: str
    lastDay: date
    style: Optional[str]
    isExpired: bool
    tracks: list[int]


@dataclass
class BattleDataResponse:
    categories: list[RateCategoryEntity]
    rounds: list[RoundWithTracksDTO]


class FetchBattleDataService:

    def __init__(self, battle_data_dao: BattleDataDAO):
        self.battle_data_dao = battle_data_dao

    def execute(self) -> BattleDataResponse:
        categories = self.battle_data_dao.fetch_rate_categories()

        rounds_with_tracks_dtos = []
        round_tracks_dtos = self.battle_data_dao.fetch_rounds_with_tracks()
        for round_tracks_dto in round_tracks_dtos:
            rates = self.battle_data_dao.fetch_rates(round_id=round_tracks_dto.round.id)

            track_id_rates_map = defaultdict(list)
            for rate in rates:
                track_id_rates_map[rate.track_id].append(rate)

            round_entity = round_tracks_dto.round
            round_with_tracks_dto = RoundWithTracksDTO(
                id=round_entity.id,
                number=round_entity.number,
                theme=round_entity.theme,
                type=round_entity.type,
                lastDay=round_entity.last_day,
                style=round_entity.style,
                isExpired=date.today() > round_entity.last_day,
                tracks=[],
            )

            tracks_with_rates_dtos = []
            for track_entity in round_tracks_dto.tracks:
                track_with_rates_dto = TrackWithRatesDTO(
                    id=track_entity.id,
                    name=track_entity.name,
                    userId=track_entity.user_id,
                    userUsername=track_entity.user_username,
                    userColor=f'#{track_entity.user_color}',
                    rates=[],
                )
                rates_dtos = []
                for rate in track_id_rates_map[track_entity.id]:
                    rate_dto = RateDTO(
                        categoryId=rate.category_id,
                        userId=rate.user_id,
                        userUsername=rate.user_username,
                        userColor=f'#{rate.user_color}',
                    )
                    rates_dtos.append(rate_dto)

                track_with_rates_dto.rates = rates_dtos
                tracks_with_rates_dtos.append(track_with_rates_dto)

            round_with_tracks_dto.tracks = tracks_with_rates_dtos
            rounds_with_tracks_dtos.append(round_with_tracks_dto)

        return BattleDataResponse(
            categories=categories,
            rounds=rounds_with_tracks_dtos,
        )
