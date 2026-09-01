from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class GraphQLError:

    message: str
    path: list[str] | None = None
    code: int | None = None
    details: str | None = None


@dataclass(slots=True)
class GraphQLResponse:

    data: dict[str, Any] | None = None

    errors: list[GraphQLError] = field(default_factory=list)

    extensions: dict[str, Any] | None = None

    @property
    def success(self) -> bool:
        return len(self.errors) == 0

    @property
    def has_errors(self) -> bool:
        return not self.success