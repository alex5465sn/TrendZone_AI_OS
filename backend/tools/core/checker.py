from abc import ABC
from abc import abstractmethod

from tools.core.report import AuditReport


class Checker(ABC):

    NAME = ""

    DESCRIPTION = ""

    VERSION = "1.0"

    @abstractmethod
    def run(
        self,
        report: AuditReport,
    ) -> None:
        ...