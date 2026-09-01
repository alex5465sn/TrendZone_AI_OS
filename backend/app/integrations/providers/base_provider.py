"""
TrendZone AI OS
================================

Base Provider

Interface oficial para qualquer
Marketplace integrado ao sistema.

Todos os Providers devem implementar
os mesmos métodos.
"""

from abc import ABC
from abc import abstractmethod


class BaseProvider(ABC):

    @abstractmethod
    def search_products(
        self,
        **kwargs,
    ):
        ...

    @abstractmethod
    def search_shops(
        self,
        **kwargs,
    ):
        ...

    @abstractmethod
    def search_offers(
        self,
        **kwargs,
    ):
        ...

    @abstractmethod
    def generate_short_link(
        self,
        url: str,
        sub_ids=None,
    ):
        ...

    @abstractmethod
    def conversion_report(
        self,
        **kwargs,
    ):
        ...