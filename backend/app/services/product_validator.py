"""
TrendZone AI OS
================================

Product Validator.

Responsável exclusivamente pela
validação de produtos antes de
entrarem no Pipeline IA.

Não calcula Score.

Não salva no banco.

Não toma decisões.
"""

from app.core.exceptions import ValidationException

from app.services.base_service import BaseService


class ProductValidator(BaseService):
    """
    Validador oficial do TrendZone AI OS.
    """

    SERVICE_NAME = "PRODUCT_VALIDATOR"

    REQUIRED_FIELDS = (

        "item_id",

        "shop_id",

        "name",

        "price",

        "commission",

        "rating",

        "sales",

    )

    @classmethod
    def validate(
        cls,
        product: dict,
    ) -> bool:

        cls.log_info(
            "Validando produto..."
        )

        for field in cls.REQUIRED_FIELDS:

            if field not in product:

                cls.log_error(
                    f"Campo obrigatório ausente: {field}"
                )

                raise ValidationException(
                    f"Campo obrigatório ausente: {field}"
                )

        if not product["name"].strip():

            raise ValidationException(
                "Nome inválido."
            )

        if product["price"] <= 0:

            raise ValidationException(
                "Preço inválido."
            )

        if product["commission"] < 0:

            raise ValidationException(
                "Comissão inválida."
            )

        if product["rating"] < 0:

            raise ValidationException(
                "Avaliação inválida."
            )

        if product["sales"] < 0:

            raise ValidationException(
                "Quantidade de vendas inválida."
            )

        cls.log_success(
            "Produto validado."
        )

        return True