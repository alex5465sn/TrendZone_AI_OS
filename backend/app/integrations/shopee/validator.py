from typing import Optional


class ShopeeValidator:

    @staticmethod
    def validate_token(
        token: Optional[str],
    ):

        if not token:
            raise ValueError(
                "Access Token não informado."
            )

    @staticmethod
    def validate_query(
        query: str,
    ):

        if not query.strip():
            raise ValueError(
                "GraphQL Query vazia."
            )

    @staticmethod
    def validate_variables(
        variables: Optional[dict],
    ):

        if variables is not None:

            if not isinstance(
                variables,
                dict,
            ):
                raise TypeError(
                    "Variables deve ser um dict."
                )