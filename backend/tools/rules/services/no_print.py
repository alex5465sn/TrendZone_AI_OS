from tools.rules.base_rule import BaseRule

from tools.core.finding import Finding
from tools.core.severity import Severity
from tools.core.ast_utils import ASTUtils


class NoPrintRule(BaseRule):

    ID = "TZ101"

    TITLE = "No Print"

    DESCRIPTION = "Não utilizar print() em Services."

    def execute(
        self,
        file,
        tree,
    ):

        findings = []

        for call in ASTUtils.calls(tree):

            if call == "print":

                findings.append(

                    Finding(

                        checker="Services",

                        severity=Severity.WARNING,

                        file=str(file),

                        line=None,

                        rule=self.ID,

                        message="print() encontrado.",

                        recommendation="Utilizar Logger.",

                    )

                )

        return findings