from tools.core.python_checker import PythonProjectChecker
from tools.core.finding import Finding
from tools.core.report import AuditReport
from tools.core.severity import Severity


class ApiChecker(PythonProjectChecker):

    NAME = "API"

    DESCRIPTION = "API Validation"

    VERSION = "1.0"

    def run(self, report: AuditReport):

        for file in self.python_files():

            if "app/api" not in str(file).replace("\\", "/"):
                continue

            tree = self.parse(file)

            imports = self.imports(tree)

            if any("sqlalchemy" in str(i).lower() for i in imports):

                report.add(

                    Finding(

                        checker=self.NAME,

                        severity=Severity.ERROR,

                        file=str(file),

                        line=None,

                        rule="TZ015",

                        message="API acessando SQLAlchemy diretamente.",

                        recommendation="A API deve utilizar Services.",

                    )

                )

            if any("session" in str(i).lower() for i in imports):

                report.add(

                    Finding(

                        checker=self.NAME,

                        severity=Severity.WARNING,

                        file=str(file),

                        line=None,

                        rule="TZ016",

                        message="Sessão do banco encontrada na API.",

                        recommendation="Mover acesso ao banco para Repository/Service.",

                    )

                )