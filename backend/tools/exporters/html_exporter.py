class HtmlExporter:

    @staticmethod
    def export(report):

        html = """

        <html>

        <head>

        <title>TrendZone Audit</title>

        </head>

        <body>

        <h1>TrendZone Enterprise Audit</h1>

        <table border="1">

        <tr>

        <th>Severity</th>

        <th>Rule</th>

        <th>File</th>

        <th>Message</th>

        </tr>

        """

        for finding in report.findings:

            html += f"""

            <tr>

            <td>{finding.severity}</td>

            <td>{finding.rule}</td>

            <td>{finding.file}</td>

            <td>{finding.message}</td>

            </tr>

            """

        html += """

        </table>

        </body>

        </html>

        """

        return html