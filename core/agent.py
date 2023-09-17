from typing import Self

from .hand import Hand
from .tile import Tile
from .player import Player


class Agent:
    player: Player

    def set_player(self, player: Player):
        self.player = player

    def decide_sute(self: Self) -> Tile:
        tile, _ = next(iter(self.player.hand.suggestions.items()))
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
