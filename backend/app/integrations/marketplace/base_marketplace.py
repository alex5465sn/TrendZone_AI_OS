"""
TrendZone AI OS
================================

Marketplace Base

Contrato oficial para todos
os Marketplaces suportados.
"""

from abc import ABC
from abc import abstractmethod


class BaseMarketplace(ABC):

    @abstractmethod
    def search_products(

        self,

        keyword: str,

        page: int,

        limit: int,

    ):
        """
        Deve retornar uma lista
        de ProductDTO.
        """
        pass