from __future__ import annotations
from typing import Self, TYPE_CHECKING
from .tile import Tile
from .player import Player

if TYPE_CHECKING:
    from .game import OptionsInTurn


class PlayerInTurnActionType:
    REACH = "reach"
    TSUMO = "tsumo"
    ANKAN = "ankan"
    ADD_KANG = "add_kan"
    SUTE = "sute"


class PlayerInTurnAction:
    type: PlayerInTurnActionType
    tile: Tile | None = None


class Agent:
    player: Player

    def __init__(self):
        self.name = "BaselineAI"

    def set_player(self, player: Player):
        self.player = player

    def decide_sute(self: Self) -> Tile:
        tile, _ = next(iter(self.player.hand.get_one_suggestion().items()))
        return tile

    def decide_if_reach(self) -> bool:
        """决定是否立直，默认为听牌即立。

        Returns:
            bool: 是否立直
        """
        return True

    def decide_if_ron(self) -> bool:
        """是否胡牌

        Returns:
            bool: 是否胡牌
        """
        return True

    def decide_turn_action(self, options: OptionsInTurn) -> PlayerInTurnAction:
        action = PlayerInTurnAction()
        if options.reach:
            action.type = PlayerInTurnActionType.REACH
            action.tile = self.decide_sute()
        elif options.tsumo:
            action.type = PlayerInTurnActionType.TSUMO
        elif options.add_kan:
            action.type = PlayerInTurnActionType.ADD_KANG
        elif options.ankan:
            action.type = PlayerInTurnActionType.ANKAN
        else:
            action.type = PlayerInTurnActionType.SUTE
            action.tile = self.decide_sute()
        return action

    def __repr__(self) -> str:
        return self.name

    def __str__(self) -> str:
        return self.name
