from datetime import date

from daos import BattleControlDAO
from exceptions import SubmitTrackException

from models.round import RoundTypes


class SubmitTrackService:

    def __init__(self, battle_control_dao: BattleControlDAO):
        self.battle_control_dao = battle_control_dao

    def execute(
            self,
            user_id: int,
            round_id: int,
            track_name: str,
    ) -> None:
        if self.battle_control_dao.check_is_track_exists_by_round_and_user_ids(
            round_id=round_id,
            user_id=user_id,
        ):
            raise SubmitTrackException(message='Ты уже сдал трэк на этот раунд')

        round_entity = self.battle_control_dao.get_round_entity(round_id=round_id)
        if round_entity.last_day < date.today():
            raise SubmitTrackException(message='Раунд уже закончился, трэк сдать нельзя')

        if round_entity.type == RoundTypes.one_vs_one.value:
            is_pair_exists = self.battle_control_dao.check_if_pair_exists(
                round_id=round_id,
                user_id=user_id,
            )
            if not is_pair_exists:
                raise SubmitTrackException(message='Тебя нету ни в одной паре на этот батл')

        self.battle_control_dao.create_track(
            round_id=round_id,
            user_id=user_id,
            track_name=track_name,
        )
