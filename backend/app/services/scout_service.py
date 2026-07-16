"""
TrendZone AI OS
================================

Scout Service.

Responsável pelo Pipeline Oficial
de prospecção de produtos.

Pipeline

Buscar
↓

Mapear
↓

Validar
↓

Calcular Score
↓

Tomar decisão
↓

Gerar relatório
"""

from app.integrations.shopee.scout import ShopeeScout
from app.mappers.product_mapper import ProductMapper

from app.services.base_service import BaseService
from app.services.product_validator import ProductValidator
from app.services.product_score import ProductScore
from app.services.decision_engine import DecisionEngine
from app.services.executive_report import ExecutiveReport


class ScoutService(BaseService):

    SERVICE_NAME = "SCOUT_SERVICE"

    def __init__(self, db=None):

        self.db = db

        self.scout = ShopeeScout()

    # =====================================================
    # PIPELINE
    # =====================================================

    def search_products(self):

        self.log_info("Iniciando Pipeline Scout...")

        raw_products = self.fetch_products()

        products = self.map_products(raw_products)

        products = self.validate_products(products)

        products = self.score_products(products)

        products = self.decision_products(products)

        reports = self.generate_reports(products)

        self.log_success(
            f"{len(reports)} relatório(s) gerado(s)."
        )

        return reports

    # =====================================================
    # ETAPA 1
    # =====================================================

    def fetch_products(self):

        self.log_info("Buscando produtos...")

        return self.scout.get_products()

    # =====================================================
    # ETAPA 2
    # =====================================================

    def map_products(self, products):

        self.log_info("Mapeando produtos...")

        return [

            ProductMapper.from_shopee(product)

            for product in products

        ]

    # =====================================================
    # ETAPA 3
    # =====================================================

    def validate_products(self, products):

        self.log_info("Validando produtos...")

        valid_products = []

        for product in products:

            ProductValidator.validate(product)

            valid_products.append(product)

        return valid_products

    # =====================================================
    # ETAPA 4
    # =====================================================

    def score_products(self, products):

        self.log_info("Calculando Score...")

        for product in products:

            product["score"] = ProductScore.calculate(

                commission=product["commission"],

                rating=product["rating"],

                sales=product["sales"],

            )

        return products

    # =====================================================
    # ETAPA 5
    # =====================================================

    def decision_products(self, products):

        self.log_info("Classificando produtos...")

        for product in products:

            product["decision"] = DecisionEngine.classify(
                product
            )

        return products

    # =====================================================
    # ETAPA 6
    # =====================================================

    def generate_reports(self, products):

        self.log_info("Gerando relatórios...")

        reports = []

        for product in products:

            reports.append(

                ExecutiveReport.build(product)

            )

        return reports