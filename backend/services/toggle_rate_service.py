from daos import BattleControlDAO

from models.round import RoundTypes


class ToggleRateService:

    def __init__(self, battle_control_dao: BattleControlDAO):
        self.battle_control_dao = battle_control_dao

    def execute(
            self,
            round_id: int,
            category_id: int,
            track_id: int,
            user_id: int,
    ) -> None:
        if self.battle_control_dao.get_track_user_id(track_id=track_id) == user_id:
            return

        rate_already_exists = self.battle_control_dao.check_if_rate_exists(
            round_id=round_id,
            category_id=category_id,
            track_id=track_id,
            user_id=user_id,
        )

        round_entity = self.battle_control_dao.get_round_entity(round_id=round_id)

        if round_entity.type == RoundTypes.all_vs_all.value:
            self.battle_control_dao.delete_rate_for_category(
                round_id=round_id,
                category_id=category_id,
                user_id=user_id,
            )
        else:
            pair_entity = self.battle_control_dao.get_pair_entity(
                round_id=round_id,
                track_id=track_id,
            )
            self.battle_control_dao.delete_rate_for_pair_and_category(
                round_id=round_id,
                category_id=category_id,
                user_id=user_id,
                pair_entity=pair_entity,
            )

        if rate_already_exists:
            return

        self.battle_control_dao.create_rate(
            round_id=round_id,
            category_id=category_id,
            track_id=track_id,
            user_id=user_id,
        )


