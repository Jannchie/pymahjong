from __future__ import annotations
import enum
from typing import TYPE_CHECKING
from .hand import Hand, get_str_list
from .tile import Tile

if TYPE_CHECKING:
    from .game import Game


class FuruType(enum.Enum):
    PON = "PON"
    CHI = "CHI"
    KAN = "KAN"
    ANKAN = "ANKAN"


class Sute:
    def __init__(self, tile: Tile, is_tsumogiri: bool = False):
        self.tile = tile
        self.is_tsumogiri = is_tsumogiri

    def __repr__(self) -> str:
        return f"<{'摸' if self.is_tsumogiri else '手'}切{self.tile}>"

    def __str__(self) -> str:
        return get_str_list(self)


class Furu:
    def __init__(self, tiles: list[Tile], sute: Tile, type: FuruType):
        self.tiles = tiles
        self.sute = sute
        self.type = type

    def __str__(self) -> str:
        return get_str_list(self)

    def __repr__(self) -> str:
        return f"<{self.tiles}>"


class Player:
    def __init__(
        self,
        hand: Hand = [],
        sute: list[Sute] = [],
        furu: list[Furu] = [],
        game: Game = None,
    ):
        self.hand = hand
        self.sute = sute
        self.furu = furu
        self.game = game
        self.reach = False

    def kire(self, tile: Tile):
        self.hand.remove(tile)
        self.sute.append(tile)

    def can_kan(self, tile: Tile) -> bool:
        cnt = 0
        for t in self.hand:
            if t == tile:
                cnt += 1
        return cnt >= 3

    def ankan_options(self) -> tuple[Tile]:
        res = []
        for t in self.hand.counter:
            if self.hand.counter[t] == 4:
                res.append(t)

        if self.reach:
            suggest = self.hand.get_suggestion()
            for option in res:
                hand = Hand(self.hand[:])
                for t in hand:
                    # 尝试取出暗杠牌
                    if t == option:
                        hand.remove(t)
                new_suggest = hand.get_suggestion()
                if new_suggest != suggest:
                    # 如果暗杠后的手牌建议不同，则不允许暗杠
                    res.remove(option)
        return tuple(res)

    def can_add_kan(self, target: Tile) -> Furu | None:
        for f in self.furu:
            if f.type == FuruType.PON and f.tiles[0] == target:
                return f
        return None

    def add_kan(self, furu: Furu, tile: Tile):
        furu.tiles.append(tile)
        furu.type = FuruType.KAN
        self.hand.kire(tile)

    def reach_options(self) -> tuple[Tile]:
        if self.reach:
            return tuple()

    def ankan(self, tile: Tile):
        should_remove = []
        for t in self.hand:
            should_remove.append(t)
        self.furu.append(Furu([tile] + should_remove, tile, FuruType.ANKAN))
        for t in should_remove:
            self.hand.remove(t)

    def kan(self, tile: Tile) -> bool:
        should_remove = []
        self.furu.append(Furu([tile], tile, FuruType.KAN))
        for t in self.hand:
            if t == tile:
                should_remove.append(t)

        for t in should_remove:
            self.hand.remove(t)
        self.furu[-1].tiles += should_remove

        if self.game:
            # 摸岭上牌
            self.hand.append(self.game.dead_wall.pop(0))
            # TODO: 应该等待先打一张，再翻宝牌
            # 翻新宝牌
            self.game.dora_num += 1

    def can_pon(self, tile: Tile) -> bool:
        cnt = 0
        for t in self.hand:
            if t == tile:
                cnt += 1
        return cnt >= 2

    def can_chi(self, tile: Tile) -> bool:
        test = [0, 0, 0, 0]
        for t in self.hand:
            if t.suit != tile.suit:
                continue
            if t.val == tile.val - 2:
                test[0] += 1
                if test[1] > 0:
                    return True
            elif t.val == tile.val - 1:
                test[1] += 1
                if test[0] > 0 or test[2] > 0:
                    return True
            elif t.val == tile.val + 1:
                test[2] += 1
                if test[1] > 0 or test[3] > 0:
                    return True
            elif t.val == tile.val + 2:
                test[3] += 1
                if test[2] > 0:
                    return True
        return False

    def pon(self, target: Tile, hand: tuple[Tile]):
        self.hand.kire(hand[0])
        self.hand.kire(hand[1])
        self.furu.append(Furu([target, hand[0], hand[1]], target, FuruType.PON))

    def chi(self, target: Tile, hand: tuple[Tile]):
        self.hand.kire(hand[0])
        self.hand.kire(hand[1])
        self.furu.append(Furu([target, hand[0], hand[1]], target, FuruType.CHI))

    def print_info(self):
        print(f"=====================================")
        print(f"目前 {self.hand.get_syanten(False)} 向听")
        print(f"手牌: {get_str_list(self.hand)}")
        print(f"副露: {get_str_list(self.furu)}")
        print(f"切牌: {get_str_list(self.sute)}")

    def has_kan_chi_pon(self, player):
        has_kan_chi_pon = False
        for f in player.furu:
            if f.type in (FuruType.KAN, FuruType.PON, FuruType.CHI):
                has_kan_chi_pon = True
                break
        return has_kan_chi_pon
