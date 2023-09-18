from __future__ import annotations
from typing import TYPE_CHECKING
from random import shuffle

from .player import Furu, FuruType, Player, Sute
from .hand import Hand, get_str_list
from .tile import Tile
from .utils import ALL
from .agent import (
    Agent,
    InTurnActionType,
    OptionsInTurn,
    OptionsOutOfTurn,
    OutOfTurnAction,
    OutofTurnActionType,
)

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
            p = Player(hand=Hand(self.wall[:13]), game=self, sute=[], furu=[])
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

    def get_rinsyan(self, player: Player):
        player.hand.append(self.dead_wall.pop())

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

    async def start(self):
        print("")
        print("########")
        print("开始对局")
        print("########")
        self.print_info()
        t = 0
        next_player = None
        for idx, agent in self.agents.items():
            print(f"对玩家<{agent}>起手配牌")
            agent.set_player(self.players[idx])
        while self.wall:
            self.junmei = t // 4 + 1
            cur_player_idx = t % 4
            agent = self.agents[cur_player_idx]
            player = self.players[cur_player_idx]
            if next_player:
                next_player = None
                log = f"玩家<{agent}>准备打牌 "
                can_kan = False
            else:
                tsumohai = self.tsumo(cur_player_idx)
                log = f"玩家<{agent}>摸{tsumohai}, "
                can_kan = True
            if self.junmei == 1:
                # TODO: 检查是否九种九牌
                # TODO: 检查是否四风连打
                pass

            reach_in_this_junmei = False  # 是否在该巡目立直

            should_add_dora = False  # 是否需要翻宝牌（因为明杠）
            # 如果进行的是暗杠或者加杠，则可能重复这段操作，否则退出循环
            while True:
                in_turn_options = self.get_options(player, tsumohai, can_kan)

                # TODO：如果开启包牌规则，杠后自摸，被杠人支付点数
                # TODO: 杠行为后，需要判断能否抢杠

                in_turn_action = agent.decide_in_turn(in_turn_options)

                if (
                    in_turn_action.type == InTurnActionType.REACH
                    and in_turn_options.reach
                ):
                    # 立直
                    sutehai = in_turn_options.reach[in_turn_action.choice]
                    reach_in_this_junmei = True
                    break  # 打牌，结束循环
                elif (
                    in_turn_action.type == InTurnActionType.TSUMO
                    and in_turn_options.tsumo
                ):
                    # 自摸，结束对局
                    # TODO: 计算番数、点棒流转
                    log += "自摸!"
                    print(log)
                    return
                elif (
                    in_turn_action.type == InTurnActionType.ADD_KANG
                    and in_turn_options.add_kan
                ) or (
                    in_turn_action.type == InTurnActionType.ANKAN
                    and in_turn_options.ankan
                ):  # 杠
                    # 如果之前有明杠，则需要先翻宝牌
                    if should_add_dora:
                        self.dora_num += 1
                        should_add_dora = False

                    if in_turn_action.type == InTurnActionType.ADD_KANG:
                        player.add_kan(in_turn_options.add_kan, tsumohai)
                        self.rinsyan = True

                        # print('摸岭上牌1')
                        # print(tsumohai)
                        # print(agent.player.furu)

                        # 摸岭上牌
                        self.get_rinsyan(player)

                        # 需要之后翻宝牌
                        should_add_dora = True
                    else:
                        player.ankan(in_turn_options.ankan[in_turn_action.choice])

                        # 翻宝牌
                        self.dora_num += 1

                        # TODO：判断是否四杠散了

                        # 摸岭上牌
                        self.get_rinsyan(player)

                elif in_turn_action.type == InTurnActionType.SUTE:
                    sutehai = player.hand[in_turn_action.choice]
                    break  # 打牌，结束循环
                else:
                    print("不合法的操作！回退到摸切！")
                    in_turn_action.type = InTurnActionType.SUTE
                    sutehai = tsumohai
                    break  # 打牌，结束循环

            # 执行打牌操作
            if tsumohai is sutehai:
                log += f"摸切{sutehai}, "
                player.sute.append(Sute(sutehai, True))
            else:
                log += f"手切{sutehai}, "
                player.sute.append(Sute(sutehai, False))

            if reach_in_this_junmei:
                log += "宣布立直！"

            player.hand.kire(sutehai)

            if should_add_dora:
                self.dora_num += 1
                should_add_dora = False

            action_and_options = []
            action: OutOfTurnAction = None
            options: OptionsOutOfTurn = None

            # 所有别家，同时判断是否能够吃、碰、杠、荣胡。
            for i in range(len(self.players)):
                if i == cur_player_idx:
                    continue
                options = OptionsOutOfTurn()
                h = Hand(self.players[i].hand)

                # 先判断是否可以吃碰杠
                options.pon = h.pon_options(sutehai)
                options.chi = h.chi_options(sutehai)
                options.kan = h.kan_options(sutehai)

                # 把牌放进手牌，判断是否能够荣胡
                h.append(sutehai)
                options.ron = h.syanten == -1
                action = await self.agents[i].decide_out_of_turn(options)
                if action:
                    action_and_options.append((action, options))

            if action_and_options:
                # 优先级
                # TODO：需要判断各个玩家操作的优先级，并执行最高优先级的操作。
                # TODO：一般，荣胡>杠=碰>吃，可能有不同规则。
                p = {
                    OutofTurnActionType.RON: 4,
                    OutofTurnActionType.KAN: 3,
                    OutofTurnActionType.PON: 2,
                    OutofTurnActionType.CHI: 1,
                }
                action, options = sorted(
                    action_and_options, key=lambda x: p[x[0].type], reverse=True
                )[0]

                if action.type == OutofTurnActionType.RON:
                    # 荣胡
                    log += f"{agent}放炮，<{action.agents}>荣胡!"
                    print(log)
                    return
                elif action.type == OutofTurnActionType.CHI:
                    # 吃
                    log += f"<{action.agent}>吃!"
                    action.agent.player.chi(sutehai, options.chi[action.choice])
                    next_player = action.agent.player
                elif action.type == OutofTurnActionType.PON:
                    # 碰
                    log += f"<{action.agent}>碰!"
                    action.agent.player.pon(sutehai, options.pon[action.choice])
                    next_player = action.agent.player
                elif action.type == OutofTurnActionType.KAN:
                    # 杠
                    log += f"<{action.agent}>杠!!"
                    action.agent.player.kan(sutehai, options.kan[action.choice])

                    # 翻宝牌
                    self.dora_num += 1

                    # TODO：判断是否四杠散了

                    # 摸岭上牌
                    self.get_rinsyan(action.agent.player)
                    next_player = action.agent.player

            if reach_in_this_junmei:
                player.reach = True
                # TODO: 立直成功，支付 1000 点棒
                log += "无人胡牌，立直成功！支付 1000 点棒!"

            print(log)

            if next_player:
                idx = self.players.index(next_player)
                while t % 4 != idx:
                    t += 1
            else:
                t += 1
        print("荒牌流局")

    def get_options(self, player: Player, tsumohai: Tile, can_kan: bool):
        syanten = player.hand.syanten  # 获取当前向听数
        options = OptionsInTurn()
        if player.reach:
            # 如果已经立直
            if syanten == -1:
                # 如果已经自摸
                options.tsumo = True

            # 如果能够暗杠（不改变听牌）
            options.ankan = player.ankan_options()
        else:
            # 自家，需要同时判断是否能立直、自摸、暗杠或加杠。
            # 吃碰杠后需要打出一张牌
            # 杠完还需要翻新宝牌指示牌和摸岭上牌
            # 获取暗杠选项

            # 允许手切
            options.tegiri = True

            # 吃碰之后不能直接杠
            if can_kan:
                # 判断能否暗杠
                options.ankan = player.ankan_options()
                # 判断能否加杠
                options.add_kan = player.can_add_kan(tsumohai)

            # 判断是否能自摸
            if syanten == -1:
                options.tsumo = True

                # 判断是否能立直
                # 1. 如果不是最后一巡
                # 2. 当前处于听牌状态
                # 3. 没有明杠、吃、碰。
                # TODO: 4. 有 1000 点棒
            has_kan_chi_pon = self.has_kan_chi_pon(player)

            if (
                (len(self.wall) >= 4 or self.config.last_junmei_reach)
                and syanten == 0
                and not has_kan_chi_pon
            ):
                options.reach = tuple(player.hand.suggestions.keys())
        return options

    def has_kan_chi_pon(self, player):
        has_kan_chi_pon = False
        for f in player.furu:
            if f.type in (FuruType.KAN, FuruType.PON, FuruType.CHI):
                has_kan_chi_pon = True
                break
        return has_kan_chi_pon
