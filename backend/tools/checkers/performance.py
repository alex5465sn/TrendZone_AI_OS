from tools.core.python_checker import PythonProjectChecker
from tools.core.finding import Finding
from tools.core.report import AuditReport
from tools.core.severity import Severity


class PerformanceChecker(PythonProjectChecker):

    NAME = "Performance"

    DESCRIPTION = "Performance Validation"

    VERSION = "1.0"

    def run(self, report: AuditReport):

        for file in self.python_files():

            tree = self.parse(file)

            calls = self.calls(tree)

            if "sleep" in calls:

                report.add(

                    Finding(

                        checker=self.NAME,

                        severity=Severity.WARNING,

                        file=str(file),

                        line=None,

                        rule="TZ017",

                        message="Uso de sleep() encontrado.",

                        recommendation="Evitar bloqueios síncronos.",

                    )

                )

            if "requests" in calls:

                report.add(

                    Finding(

                        checker=self.NAME,

                        severity=Severity.INFO,

                        file=str(file),

                        line=None,

                        rule="TZ018",

                        message="Cliente HTTP síncrono detectado.",

                        recommendation="Avaliar uso de httpx assíncrono quando apropriado.",

                    )

                )