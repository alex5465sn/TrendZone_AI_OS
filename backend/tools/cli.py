"""
TrendZone AI OS

CLI
"""

from tools.audit import EnterpriseAudit


class AuditCLI:

    @staticmethod
    def execute():

        report = EnterpriseAudit().execute()

        print()

        print("=" * 70)
        print("TrendZone AI OS Enterprise Audit")
        print("=" * 70)

        severities = report.by_severity()

        print()

        print(f"INFO      : {severities.get('INFO',0)}")
        print(f"WARNING   : {severities.get('WARNING',0)}")
        print(f"ERROR     : {severities.get('ERROR',0)}")
        print(f"CRITICAL  : {severities.get('CRITICAL',0)}")

        print()

        print(f"Enterprise Score : {report.score()}%")

        print()

        for finding in report.findings:

            print("-"*70)

            print(f"[{finding.severity}] {finding.rule}")

            print(f"Checker : {finding.checker}")

            print(f"Arquivo : {finding.file}")

            if finding.line:

                print(f"Linha   : {finding.line}")

            print(f"Problema: {finding.message}")

            print(f"Solução : {finding.recommendation}")

        print()

        print("="*70)


if __name__ == "__main__":

    AuditCLI.execute()