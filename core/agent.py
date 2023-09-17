from typing import Self

from .hand import Hand
from .tile import Tile
from .player import Player


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

    def __repr__(self) -> str:
        return self.name

    def __str__(self) -> str:
        return self.name
