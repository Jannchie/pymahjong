from typing_extensions import override
from core.hand import Hand


class Yaku:
    def __init__(self, han) -> None:
        self.han = int(han)
        pass

    @staticmethod
    def check(h: Hand) -> bool:
        raise NotImplementedError


class Tanyao(Yaku):
    def __init__(self) -> None:
        super().__init__(1)

    @override
    def check(h: Hand) -> bool:
        return all([not i.is_yaochu for i in h])


class Kokushimusou(Yaku):
    def __init__(self) -> None:
        super().__init__(13)

    @override
    def check(h: Hand) -> bool:
        return h.syanten == -1 and h[0].is_yaochu
