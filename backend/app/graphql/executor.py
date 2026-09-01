"""
TrendZone AI OS
================================

GraphQL Executor
"""

from app.integrations.shopee.graphql.client import GraphQLClient
from app.integrations.shopee.graphql.auth import ShopeeAuth


class GraphQLExecutor:

    def __init__(self):

        self.client = GraphQLClient()

    def execute(

        self,

        query: str,

        variables=None,

    ):

        return self.client.execute(

            query=query,

            variables=variables,

            headers=ShopeeAuth.headers(),

        )