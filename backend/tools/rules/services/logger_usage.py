from tools.rules.base_rule import BaseRule

from tools.core.finding import Finding
from tools.core.severity import Severity
from tools.core.ast_utils import ASTUtils


class LoggerUsageRule(BaseRule):

    ID = "TZ103"

    TITLE = "Logger"

    DESCRIPTION = "Service deve utilizar Logger."

    def execute(
        self,
        file,
        tree,
    ):

        findings = []

        imports = ASTUtils.imports(tree)

        logger_imported = False

        for module in imports:

            if module and "logger" in module.lower():

                logger_imported = True

        if not logger_imported:

            findings.append(

                Finding(

                    checker="Services",

                    severity=Severity.INFO,

                    file=str(file),

                    line=None,

                    rule=self.ID,

                    message="Logger não encontrado.",

                    recommendation="Utilizar app.core.logger.",

                )

            )

        return findings