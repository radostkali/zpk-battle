from daos import BattleControlDAO


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
        if self.battle_control_dao.get_tracks_user_id(track_id=track_id) == user_id:
            return

        if self.battle_control_dao.check_if_rate_exists(
            round_id=round_id,
            category_id=category_id,
            track_id=track_id,
            user_id=user_id,
        ):
            self.battle_control_dao.delete_rate_for_category(
                round_id=round_id,
                category_id=category_id,
                user_id=user_id,
            )
            return

        self.battle_control_dao.delete_rate_for_category(
            round_id=round_id,
            category_id=category_id,
            user_id=user_id,
        )
        self.battle_control_dao.create_rate(
            round_id=round_id,
            category_id=category_id,
            track_id=track_id,
            user_id=user_id,
        )


