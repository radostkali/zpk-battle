from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from typing import Optional

from entities import RateCategoryEntity
from daos import BattleDataDAO
from models.round import RoundTypes


@dataclass
class RateDTO:
    categoryId: int
    userId: int
    userUsername: str
    userColor: str


@dataclass
class TrackDTO:
    id: int
    name: str
    userId: int
    userUsername: str
    userColor: str
    rates: []


@dataclass
class PairDTO:
    tracks: list[TrackDTO]


@dataclass
class RoundDTO:
    id: int
    number: int
    theme: str
    type: str
    lastDay: date
    style: Optional[str]
    isExpired: bool
    tracks: list[TrackDTO]
    pairs: list[PairDTO]


@dataclass
class BattleDataResponse:
    categories: list[RateCategoryEntity]
    rounds: list[RoundDTO]


class FetchBattleDataService:

    def __init__(self, battle_data_dao: BattleDataDAO):
        self.battle_data_dao = battle_data_dao

    def _fetch_tracks_for_all_vs_all_round(self, round_id: int) -> list[TrackDTO]:
        rate_entities_generator = self.battle_data_dao.fetch_rates_by_round_id(
            round_id=round_id,
        )
        track_id_rates_map = defaultdict(list)
        for rate in rate_entities_generator:
            track_id_rates_map[rate.track_id].append(rate)

        tracks_entities_generator = self.battle_data_dao.fetch_tracks_by_round_id(
            round_id=round_id,
        )
        track_dto_list = []
        for track_entity in tracks_entities_generator:
            track_dto = TrackDTO(
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

            track_dto.rates = rates_dtos
            track_dto_list.append(track_dto)

        return track_dto_list

    def _fetch_tracks_for_one_vs_one_round(self, round_id: int) -> list[PairDTO]:
        rate_entities_generator = self.battle_data_dao.fetch_rates_by_round_id(
            round_id=round_id,
        )
        track_id_rates_map = defaultdict(list)
        for rate in rate_entities_generator:
            track_id_rates_map[rate.track_id].append(rate)

        tracks_entities_generator = self.battle_data_dao.fetch_tracks_by_round_id(
            round_id=round_id,
        )
        user_id_track_entity_map = {
            track.user_id: track for track in tracks_entities_generator
        }

        pair_entities_generator = self.battle_data_dao.fetch_pairs_by_round_id(
            round_id=round_id,
        )
        pair_dto_list = []
        for pair_entity in pair_entities_generator:
            pair_users_ids = (pair_entity.user_one_id, pair_entity.user_two_id, pair_entity.user_three_id)
            track_dto_list = []
            for pair_user_id in pair_users_ids:
                track_entity = user_id_track_entity_map.get(pair_user_id)
                if not track_entity:
                    continue

                track_dto = TrackDTO(
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

                track_dto.rates = rates_dtos
                track_dto_list.append(track_dto)

            if track_dto_list:
                pair_dto_list.append(PairDTO(tracks=track_dto_list))

        return pair_dto_list

    def execute(self) -> BattleDataResponse:
        categories = self.battle_data_dao.fetch_rate_categories()

        rounds_with_tracks_dtos = []
        rounds_entities_generator = self.battle_data_dao.fetch_rounds()
        for round_entity in rounds_entities_generator:
            round_dto = RoundDTO(
                id=round_entity.id,
                number=round_entity.number,
                theme=round_entity.theme,
                type=round_entity.type,
                lastDay=round_entity.last_day,
                style=round_entity.style,
                isExpired=date.today() > round_entity.last_day,
                tracks=[],
                pairs=[],
            )

            if round_entity.type == RoundTypes.all_vs_all.value:
                track_dto_list = self._fetch_tracks_for_all_vs_all_round(round_id=round_entity.id)
                round_dto.tracks = track_dto_list
            else:
                pair_dto_list = self._fetch_tracks_for_one_vs_one_round(round_id=round_entity.id)
                round_dto.pairs = pair_dto_list

            rounds_with_tracks_dtos.append(round_dto)

        return BattleDataResponse(
            categories=categories,
            rounds=rounds_with_tracks_dtos,
        )
