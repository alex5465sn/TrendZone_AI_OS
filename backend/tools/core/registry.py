from tools.core.checker import Checker


class CheckerRegistry:

    def __init__(self):

        self._items: list[Checker] = []

    def register(
        self,
        checker: Checker,
    ):

        self._items.append(checker)

    @property
    def items(self):

        return tuple(self._items)