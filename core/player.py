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


class Furu:
    def __init__(self, tiles: list[Tile], sute: Tile, type: FuruType):
        self.tiles = tiles
        self.sute = sute
        self.type = type


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

    def can_ankan(self) -> Tile:
        for t in self.hand.counter:
            if self.hand.counter[t] >= 4:
                return t
        return None

    def can_add_kan(self, target: Tile) -> Furu | None:
        for f in self.furu:
            if f.type == FuruType.PON and f.tiles[0] == target:
                return f
        return None

    def ankan(self, tile: Tile):
        if self.hand.counter[tile] == 3:
            should_remove = []
            for t in self.hand:
                should_remove.append(t)
            self.furu.append(Furu([tile] + should_remove, tile, FuruType.ANKAN))
            for t in should_remove:
                self.hand.remove(t)
        else:
            raise Exception("手牌中没有四张这张牌")

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

    def pon_options(self, tile: Tile) -> tuple((Tile, Tile)):
        tmp = []
        for t in self.hand:
            if t == tile:
                tmp.append(t)
        opts = dict()
        for i in range(len(tmp)):
            for j in range(i + 1, len(tmp)):
                peer = (tmp[i], tmp[j])
                opts[str(peer)] = peer
        return tuple(opts.values())

    def pon(self, tile: Tile, option_idx: int):
        options = self.pon_options(tile)
        option = options[option_idx]
        self.hand.remove(tile)
        self.furu.append((tile, option[0], option[1]))

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

    def chi_options(self, tile: Tile) -> tuple((Tile, Tile)):
        test = [[], [], [], []]
        for t in self.hand:
            if t.val == tile.val - 2:
                test[0].append(t)
            elif t.val == tile.val - 1:
                test[1].append(t)
            elif t.val == tile.val + 1:
                test[2].append(t)
            elif t.val == tile.val + 2:
                test[3].append(t)
        opts = dict()
        for i in range(3):
            j = i + 1
            for a in test[i]:
                for b in test[j]:
                    peer = (a, b)
                    opts[str(peer)] = peer
        return tuple(opts.values())

    def chi(self, target: Tile, option_idx: int) -> tuple((Tile, Tile)):
        options = self.chi_options(target)
        option = options[option_idx]
        for t in option:
            self.hand.kire(t)
        self.furu.append(Furu([target, option[0], option[1]], target, FuruType.CHI))

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
