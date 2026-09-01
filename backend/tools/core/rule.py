from dataclasses import dataclass
from collections.abc import Callable

from tools.core.finding import Finding


@dataclass(slots=True)
class Rule:

    id: str

    title: str

    description: str

    validator: Callable[[], list[Finding]]