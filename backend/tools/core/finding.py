from dataclasses import dataclass

from tools.core.severity import Severity


@dataclass(slots=True)
class Finding:
    """
    Representa um problema encontrado
    durante uma auditoria.
    """

    checker: str

    severity: Severity

    file: str

    line: int | None

    rule: str

    message: str

    recommendation: str