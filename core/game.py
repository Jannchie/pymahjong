from random import shuffle

from core.player import Player

from .hand import Hand, get_str_list
from .tile import Tile
from .utils import ALL


class Game:
    def __init__(self, bakaze: int = 0, kyoku: int = 0, honba: int = 1):
        self.tiles = [Tile(i) for i in ALL]
        shuffle(self.tiles)
        self.dora_num = 1
        self.bakaze = bakaze
        self.kyoku = kyoku
        self.honba = honba
        self.dead_wall = self.tiles[-14:]
        self.wall = self.tiles[:-14]
        self.players: list[Player] = []
        for _ in range(4):
            p = Player(hand=Hand(self.wall[:13]))
            self.wall = self.wall[13:]
            p.hand.sort()
            self.players.append(p)

    def print_info(self):
        bakaze = ["東", "南", "西", "北"][self.bakaze]
        kyoku = ["一", "二", "三", "四"][self.kyoku]
        print(f"=====================================")
        print(f"{bakaze}{kyoku}局: {self.honba} 本場")
        print(f"親: {self.oya()}")
        print(f"宝牌指示牌: {get_str_list(self.list_dora_indicator())}")
        print(f"里宝牌指示牌: {get_str_list(self.list_uradora_indicator())}")
        print(f"宝牌: {get_str_list(self.list_dora())}")
        print(f"牌山: {get_str_list(self.wall)}")
        print(f"王牌: {get_str_list(self.dead_wall)}")
        for i in range(4):
            print(f"=====================================")
            print(f"玩家{i}目前 {self.players[i].hand.syanten} 向听")
            print(f"玩家{i}的手牌: {get_str_list(self.players[i].hand)}")
            print(f"玩家{i}的副露: {get_str_list(self.players[i].furu)}")
            print(f"玩家{i}的切牌: {get_str_list(self.players[i].sute)}")

    def oya(self) -> int:
        """获取庄家

        Returns:
            int: 庄家的 Player ID
        """
        return self.kyoku % 4

    def list_dora_indicator(self) -> list[Tile]:
        """获取宝牌指示牌

        Returns:
            list[Tile]: 宝牌指示牌列表
        """
        return self.dead_wall[: self.dora_num * 2 : 2]

    def list_uradora_indicator(self):
        """获取里宝牌指示牌

        Returns:
            list[Tile]: 里宝牌指示牌列表
        """
        return self.dead_wall[1 : self.dora_num * 2 : 2]

    def list_dora(self):
        return [item for t in self.list_dora_indicator() for item in t.dora()]

    @staticmethod
    def get_random_hand(n=13):
        code_list = ALL[::]
        shuffle(code_list)
        return Hand(sorted([Tile(i) for i in code_list[:n]]))
