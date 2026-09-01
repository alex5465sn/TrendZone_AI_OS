from tools.core.rule import Rule


class RuleEngine:

    def __init__(self):

        self.rules: list[Rule] = []

    def register(self, rule: Rule):

        self.rules.append(rule)

    def execute(self):

        findings = []

        for rule in self.rules:

            findings.extend(

                rule.validator()

            )

        return findings