from collections import Counter

from tools.core.finding import Finding
from tools.core.severity import Severity


class AuditReport:

    def __init__(self):

        self.findings: list[Finding] = []

    def add(self, finding: Finding):

        self.findings.append(finding)

    def extend(self, findings: list[Finding]):

        self.findings.extend(findings)

    @property
    def total(self):

        return len(self.findings)

    def by_severity(self):

        counter = Counter()

        for finding in self.findings:

            counter[finding.severity] += 1

        return counter

    def score(self):

        penalty = 0

        for finding in self.findings:

            match finding.severity:

                case Severity.INFO:
                    penalty += 0

                case Severity.WARNING:
                    penalty += 1

                case Severity.ERROR:
                    penalty += 5

                case Severity.CRITICAL:
                    penalty += 20

        return max(0, 100 - penalty)