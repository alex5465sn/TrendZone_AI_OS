from tools.core.python_checker import PythonProjectChecker

from tools.core.report import AuditReport

from tools.rules.services.no_print import NoPrintRule
from tools.rules.services.no_api_dependency import NoApiDependencyRule
from tools.rules.services.logger_usage import LoggerUsageRule


class ServicesChecker(PythonProjectChecker):

    NAME = "Services"

    DESCRIPTION = "Services Validation"

    VERSION = "2.0"

    RULES = [

        NoPrintRule(),

        NoApiDependencyRule(),

        LoggerUsageRule(),

    ]

    def run(
        self,
        report: AuditReport,
    ):

        for file in self.python_files():

            if "services" not in str(file):

                continue

            tree = self.parse(file)

            for rule in self.RULES:

                report.extend(

                    rule.execute(

                        file,

                        tree,

                    )

                )