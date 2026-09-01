from tools.core.python_checker import PythonProjectChecker

from tools.core.finding import Finding

from tools.core.report import AuditReport

from tools.core.severity import Severity


class SecurityChecker(

    PythonProjectChecker

):

    NAME = "Security"

    DESCRIPTION = "Security Validation"

    VERSION = "1.0"

    def run(

        self,

        report: AuditReport,

    ):

        for file in self.python_files():

            tree = self.parse(file)

            calls = self.calls(tree)

            if "eval" in calls:

                report.add(

                    Finding(

                        checker=self.NAME,

                        severity=Severity.CRITICAL,

                        file=str(file),

                        line=None,

                        rule="TZ013",

                        message="Uso de eval().",

                        recommendation="Remover eval().",

                    )

                )

            if "exec" in calls:

                report.add(

                    Finding(

                        checker=self.NAME,

                        severity=Severity.CRITICAL,

                        file=str(file),

                        line=None,

                        rule="TZ014",

                        message="Uso de exec().",

                        recommendation="Remover exec().",

                    )

                )