from enum import Enum


class Severity(str, Enum):
    """
    Severidade dos Findings.
    """

    INFO = "INFO"

    WARNING = "WARNING"

    ERROR = "ERROR"

    CRITICAL = "CRITICAL"