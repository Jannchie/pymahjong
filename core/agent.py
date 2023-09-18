from __future__ import annotations
from typing import Self, TYPE_CHECKING
from .tile import Tile
from .player import Furu, Player


class OptionsInTurn:
    tsumo = False  # 如果可以自摸，则为 True
    add_kan: Furu | None = None  # 如果可以加杠，提供被加杠的副露
    ankan: tuple[Tile] = ()  # 如果可以暗杠，提供暗杠选项
    reach: tuple[Tile] = ()  # 如果可以立直，提供立直选项
    tegiri = False  # 如果可以手切，则为 True


class OptionsOutOfTurn:
    chi = ()
    pon = ()
    kan = ()
    ron = False


class InTurnActionType:
    REACH = "reach"
    TSUMO = "tsumo"
    ANKAN = "ankan"
    ADD_KANG = "add_kan"
    SUTE = "sute"


class OutofTurnActionType:
    RON = "ron"
    CHI = "chi"
    PON = "pon"
    KAN = "kan"
    pass


class InTurnAction:
    type: InTurnActionType
    choice: int = 0


class OutOfTurnAction:
    def __init__(self, agent: Agent) -> None:
        self.agent = agent

    type: OutofTurnActionType
    choice: int = 0


class Agent:
    player: Player

    def __init__(self):
        self.name = "BaselineAI"

    def set_player(self, player: Player):
        self.player = player

    def decide_in_turn(self, options: OptionsInTurn) -> InTurnAction:
        """决定出牌行为，默认行为：能立则立，能自摸则自摸，能加杠则加杠，能暗杠则暗杠，否则获取出牌建议，打出建议中的第一张牌。

        Args:
            options (OptionsInTurn): 当前可选操作

        Returns:
            PlayerInTurnAction: 玩家出牌行为
        """
        action = InTurnAction()
        if options.reach:
            action.type = InTurnActionType.REACH
        elif options.tsumo:
            action.type = InTurnActionType.TSUMO
        elif options.add_kan:
            action.type = InTurnActionType.ADD_KANG
        elif options.ankan:
            action.type = InTurnActionType.ANKAN
        else:
            action.type = InTurnActionType.SUTE
            tile, _ = next(iter(self.player.hand.get_one_suggestion().items()))
            action.choice = self.player.hand.index(tile)
        return action

    async def decide_out_of_turn(
        self, options: OptionsOutOfTurn
    ) -> OutOfTurnAction | None:
        action = OutOfTurnAction(self)
        if options.chi:
            action.type = OutofTurnActionType.CHI
        elif options.pon:
            action.type = OutofTurnActionType.PON
        elif options.kan:
            action.type = OutofTurnActionType.KAN
        elif options.ron:
            action.type = OutofTurnActionType.RON
        else:
            return None
        return action

    def __repr__(self) -> str:
        return self.name

    def __str__(self) -> str:
        return self.name
