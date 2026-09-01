from tools.rules.base_rule import BaseRule

from tools.core.finding import Finding
from tools.core.severity import Severity
from tools.core.ast_utils import ASTUtils


class NoApiDependencyRule(BaseRule):

    ID = "TZ102"

    TITLE = "API Dependency"

    DESCRIPTION = "Service não pode depender da API."

    def execute(
        self,
        file,
        tree,
    ):

        findings = []

        imports = ASTUtils.imports(tree)

        for module in imports:

            if module and module.startswith("app.api"):

                findings.append(

                    Finding(

                        checker="Services",

                        severity=Severity.ERROR,

                        file=str(file),

                        line=None,

                        rule=self.ID,

                        message="Dependência direta da API.",

                        recommendation="Utilizar Services desacoplados.",

                    )

                )

        return findings