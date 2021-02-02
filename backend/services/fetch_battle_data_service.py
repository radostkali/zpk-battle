from collections import defaultdict

from entities import TrackEntity, RoundEntity
from daos import BattleDataDAO


class FetchBattleDataService:

    def __init__(self, battle_data_dao: BattleDataDAO):
        self.battle_data_dao = battle_data_dao

    def _track_entity_to_dict(self, track_entity: TrackEntity) -> dict:
        return {
            'id': track_entity.id,
            'name': track_entity.name,
            'userId': track_entity.user_id,
            'userUsername': track_entity.user_username,
            'rates': [],
        }

    def _round_entity_to_dict(self, round_entity: RoundEntity) -> dict:
        return {
            'id': round_entity.id,
            'number': round_entity.number,
            'theme': round_entity.theme,
            'type': round_entity.type,
            'lastDay': round_entity.last_day,
            'style': round_entity.style,
            'tracks': [],
        }

    def execute(self) -> dict[str, list]:
        categories = self.battle_data_dao.fetch_rate_categories()

        final_rounds_dicts = []
        round_tracks_dtos = self.battle_data_dao.fetch_rounds_with_tracks()
        for round_tracks_dto in round_tracks_dtos:
            rates = self.battle_data_dao.fetch_rates(round_id=round_tracks_dto.round.id)
            track_id_rates_map = defaultdict(list)
            for rate in rates:
                track_id_rates_map[rate.track_id].append(rate)

            round_dict = self._round_entity_to_dict(round_tracks_dto.round)
            tracks_dicts = []
            for track in round_tracks_dto.tracks:
                track_dict = self._track_entity_to_dict(track)
                rates_dicts = []
                for rate in track_id_rates_map[track.id]:
                    rate_dict = {
                        'categoryId': rate.category_id,
                        'userId': rate.user_id,
                        'userUsername': rate.user_username,
                    }
                    rates_dicts.append(rate_dict)

                track_dict['rates'] = rates_dicts
                tracks_dicts.append(track_dict)

            round_dict['tracks'] = tracks_dicts
            final_rounds_dicts.append(round_dict)

        return {
            'categories': categories,
            'rounds': final_rounds_dicts,
        }
