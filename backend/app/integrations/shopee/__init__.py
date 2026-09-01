"""
TrendZone AI OS
================================

Pacote oficial da integração Shopee.

Centraliza a exportação das classes
principais utilizadas pelo sistema.

As Queries GraphQL ficam disponíveis
através do pacote graphql.
"""

from .auth import ShopeeAuth
from .client import ShopeeClient
from .gateway import ShopeeGateway
from .graphql_client import ShopeeGraphQLClient
from .graphql_executor import GraphQLExecutor

__all__ = (

    "ShopeeAuth",

    "ShopeeClient",

    "ShopeeGateway",

    "ShopeeGraphQLClient",

    "GraphQLExecutor",

)