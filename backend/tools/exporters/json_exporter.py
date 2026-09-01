import json


class JsonExporter:

    @staticmethod
    def export(report):

        return json.dumps(

            [

                {

                    "checker": finding.checker,

                    "severity": finding.severity,

                    "rule": finding.rule,

                    "file": finding.file,

                    "message": finding.message,

                    "recommendation": finding.recommendation,

                }

                for finding in report.findings

            ],

            indent=4,

            ensure_ascii=False,

        )