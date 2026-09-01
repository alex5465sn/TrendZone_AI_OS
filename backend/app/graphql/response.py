"""
TrendZone AI OS

GraphQL Response
"""


class GraphQLResponse:

    @staticmethod
    def data(response: dict):

        return response.get("data", {})

    @staticmethod
    def errors(response: dict):

        return response.get("errors", [])

    @staticmethod
    def has_errors(response: dict):

        return "errors" in response