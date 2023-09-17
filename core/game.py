from __future__ import annotations
import random
from typing import TYPE_CHECKING
from random import shuffle

from .player import Player, Sute
from .hand import Hand, get_str_list
from .tile import Tile
from .utils import ALL
from .agent import Agent

if TYPE_CHECKING:
    from .agent import Agent


class GameConfig:
    last_junmei_reach = False


class Game:
    def __init__(
        self,
        bakaze=0,
        kyoku=0,
        honba=1,
        config=GameConfig(),
    ):
        self.config = config
        self.tiles = [Tile(i) for i in ALL]
        shuffle(self.tiles)
        self.dora_num = 1
        self.bakaze = bakaze
        self.kyoku = kyoku
        self.honba = honba
        self.dead_wall = self.tiles[-14:]
        self.wall = self.tiles[:-14]
        self.players: list[Player] = []
        self.agents = {i: Agent() for i in range(4)}
        names = {
            0: "Alice",
            1: "Bob",
            2: "Carol",
            3: "Dave",
        }
        for i in range(4):
            self.agents[i].name = names[i]
            p = Player(hand=Hand(self.wall[:13]), game=self)
            self.wall = self.wall[13:]
            p.hand.sort()
            self.players.append(p)
        self.junmei = 1

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
            self.players[i].print_info()

    def oya(self) -> int:
        """获取庄家

        Returns:
            int: 庄家的 Player ID
        """
        return self.kyoku % 4

    @property
    def dora_indicator(self) -> list[Tile]:
        """宝牌指示牌列表

        Returns:
            list[Tile]: 宝牌指示牌列表
        """

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

    def link_with(self, agent: Agent, i: int):
        self.agents[i] = agent

    def tsumo(self, player_id: int):
        player = self.players[player_id]
        tsumohai = self.wall.pop()
        player.hand.append(tsumohai)
        return tsumohai

    def start(self):
        print("")
        print("########")
        print("开始对局")
        print("########")
        self.print_info()
        t = 0
        for idx, agent in self.agents.items():
            print(f"对玩家<{agent}>起手配牌")
            agent.set_player(self.players[idx])
        while self.wall:
            self.junmei = t // 4 + 1
            cur_player_id = t % 4
            agent = self.agents[cur_player_id]
            player = self.players[cur_player_id]
            tsumohai = self.tsumo(cur_player_id)

            log = ""
            log += f"玩家<{agent}>摸{tsumohai}, "

            reach_junmei = False  # 是否在该巡目立直
            syanten = player.hand.syanten  # 获取向听数

            # 判断是否胡牌
            if syanten == -1:
                # 询问是否胡牌
                if agent.decide_if_ron():
                    # 胡牌
                    # TODO: 计算番数、点棒流转
                    log += "自摸!"
                    print(log)
                    return

            if player.reach:
                # 如果已经立直
                # 立直后不允许手切
                sutehai = tsumohai
            else:
                # TODO: 同时判断是否能够吃、碰、杠、立直
                if not self.config.last_junmei_reach and len(self.wall) < 4:
                    pass  # 不允许最后一巡立直
                elif syanten == 0 and len(player.furu) == 0 and not player.reach:
                    if agent.decide_if_reach():
                        log += "立直!"
                        reach_junmei = True
                sutehai = agent.decide_sute()

            if tsumohai is sutehai:
                log += f"摸切{sutehai}, "
                player.sute.append(Sute(sutehai, True))
            else:
                log += f"手切{sutehai}, "
                player.sute.append(Sute(sutehai, False))
            player.hand.kire(sutehai)

            for i in range(len(self.players)):
                if i == cur_player_id:
                    continue
                h = Hand(self.players[i].hand)
                h.append(sutehai)
                if h.syanten == -1:
                    log += f"玩家 <{agent}> 放炮！玩家<{self.agents[i]}>荣胡！"
                    # TODO: 计算番数、点棒流转
                    print(log)
                    return
            if reach_junmei:
                player.reach = True
                # TODO: 立直成功，支付 1000 点棒
                log += "立直成功！支付 1000 点棒!"
            print(log)
            t += 1
        print("流局")
