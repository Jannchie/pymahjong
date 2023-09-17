from .hand import Hand
from .tile import Tile


class Player:
    def __init__(
        self,
        hand: Hand = [],
        sute: list[Tile] = [],
        furu: list[tuple[tuple[Tile, bool]]] = [],
    ):
        self.hand = hand
        self.sute = sute
        self.furu = furu

    def kire(self, tile: Tile):
        self.hand.remove(tile)
        self.sute.append(tile)

    def can_kan(self, tile: Tile) -> bool:
        cnt = 0
        for t in self.hand:
            if t == tile:
                cnt += 1
        return cnt >= 3

    def kan(self, tile: Tile) -> bool:
        should_remove = []
        self.furu.append([tile, False])
        for t in self.hand:
            print(t == tile, t, tile)
            if t == tile:
                should_remove.append(t)
                self.furu[-1].append([t, True])
        for t in should_remove:
            self.hand.remove(t)

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
            self.hand.remove(t)
        self.furu.append((target, option[0], option[1]))
