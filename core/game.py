from __future__ import annotations
from typing import TYPE_CHECKING
from random import shuffle

from .player import Furu, FuruType, Player, Sute
from .hand import Hand, get_str_list
from .tile import Tile
from .utils import ALL
from .agent import Agent, PlayerInTurnActionType

if TYPE_CHECKING:
    from .agent import Agent


class GameConfig:
    last_junmei_reach = False


class OptionsInTurn:
    tsumo = False
    add_kan: Furu | None = None
    ankan: Tile | None = None
    reach: [Tile] = []


class ActionsOutOfTurn:
    chi = ()
    pon = ()
    kan = ()
    ron = False


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
            cur_player_idx = t % 4
            agent = self.agents[cur_player_idx]
            player = self.players[cur_player_idx]
            tsumohai = self.tsumo(cur_player_idx)

            log = f"玩家<{agent}>摸{tsumohai}, "

            if self.junmei == 1:
                # TODO: 检查是否九种九牌
                # TODO: 检查是否四风连打
                pass

            reach_in_this_junmei = False  # 是否在该巡目立直
            syanten = player.hand.syanten  # 获取当前向听数

            # # 判断是否胡牌
            # if syanten == -1:
            #     # 询问是否胡牌
            #     if agent.decide_if_ron():
            #         # TODO: 计算番数、点棒流转
            #         log += "自摸!"
            #         print(log)
            #         return

            if player.reach:
                # 如果已经立直，可以暗杠或加杠
                # 立直后只有在不改变听牌的场合下才可以开暗杠
                # 立直之后，如果摸到原本手牌中暗刻的第四张牌，可以选择进行暗杠。
                # 如果立直时手牌中三张相同的牌不作为暗刻，暗杠的行为相当于改变了立直后的牌型，属于犯规行为。
                # 此外，也有不承认立直后的一切暗杠行为的规则。
                # 如果已经立直
                actions = OptionsInTurn()

                # TODO：判断是否自摸
                if syanten == -1:
                    log += "自摸!"
                    print(log)
                    return
                # TODO: 判断能否立直后暗杠
                actions.ankan = player.can_ankan()

                # 立直后不允许手切
                sutehai = tsumohai
            else:
                # TODO: 自家，需要同时判断是否能立直、自摸、暗杠或加杠。
                # 吃碰杠后需要打出一张牌
                # 杠完还需要翻新宝牌指示牌和摸岭上牌

                actions = OptionsInTurn()

                # 判断能否暗杠
                actions.ankan = player.can_ankan()

                # 判断能否加杠
                actions.add_kan = player.can_add_kan(tsumohai)

                # 判断是否能自摸
                if syanten == -1:
                    actions.tsumo = True

                # 判断是否能立直
                # 1. 如果不是最后一巡
                # 2. 当前处于听牌状态
                # 3. 没有明杠、吃、碰。
                # TODO: 4. 有 1000 点棒
                has_kan_chi_pon = self.has_kan_chi_pon(player)

                if (
                    syanten == 0
                    and (len(self.wall) >= 4 or self.config.last_junmei_reach)
                    and not has_kan_chi_pon
                ):
                    actions.reach = True

                # sutehai = agent.decide_sute()

            # TODO：如果开启包牌规则，杠后自摸，被杠人支付点数
            # TODO: 杠行为后，需要判断能否抢杠

            action = agent.decide_turn_action(actions)

            if action.type == PlayerInTurnActionType.REACH:
                sutehai = action.tile
                reach_in_this_junmei = True
            elif action.type == PlayerInTurnActionType.TSUMO:
                # 判断是否胡牌
                if syanten == -1:
                    # 询问是否胡牌
                    if agent.decide_if_ron():
                        # TODO: 计算番数、点棒流转
                        log += "自摸!"
                        print(log)
                        return
                else:
                    raise Exception("没有胡牌")
            elif action.type == PlayerInTurnActionType.ADD_KANG:
                # TODO: 进行加杠
                pass
            elif action.type == PlayerInTurnActionType.ANKAN:
                # TODO：进行杠
                pass
            elif action.type == PlayerInTurnActionType.SUTE:
                sutehai = action.tile
            else:
                raise Exception("未知的行为")

            if tsumohai is sutehai:
                log += f"摸切{sutehai}, "
                player.sute.append(Sute(sutehai, True))
            else:
                log += f"手切{sutehai}, "
                player.sute.append(Sute(sutehai, False))

            if reach_in_this_junmei:
                log += "宣布立直！"

            player.hand.kire(sutehai)

            # TODO: 所有别家，同时判断是否能够吃、碰、杠、荣胡。
            for i in range(len(self.players)):
                if i == cur_player_idx:
                    continue
                h = Hand(self.players[i].hand)
                h.append(sutehai)
                if h.syanten == -1:
                    log += f"玩家 <{agent}> 放炮！玩家<{self.agents[i]}>荣胡！"
                    # TODO: 计算番数、点棒流转
                    print(log)
                    return
            # TODO：需要判断各个玩家操作的优先级，并执行最高优先级的操作。
            # TODO：一般而言，荣胡>杠=碰>吃，可能有不同规则。

            if reach_in_this_junmei:
                player.reach = True
                # TODO: 立直成功，支付 1000 点棒
                log += "无人胡牌，立直成功！支付 1000 点棒!"

            print(log)
            t += 1
        print("荒牌流局")

    def has_kan_chi_pon(self, player):
        has_kan_chi_pon = False
        for f in player.furu:
            if f.type in (FuruType.KAN, FuruType.PON, FuruType.CHI):
                has_kan_chi_pon = True
                break
        return has_kan_chi_pon
