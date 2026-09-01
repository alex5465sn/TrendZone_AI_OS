class ShopeeException(Exception):
    """Exceção base da integração Shopee."""


class AuthenticationError(ShopeeException):
    """Falha de autenticação."""


class AuthorizationError(ShopeeException):
    """Permissão insuficiente."""


class InvalidTokenError(AuthenticationError):
    """Token inválido."""


class TokenExpiredError(AuthenticationError):
    """Token expirado."""


class RateLimitError(ShopeeException):
    """Limite de requisições excedido."""


class InvalidResponseError(ShopeeException):
    """Resposta inválida da API."""


class ShopeeServerError(ShopeeException):
    """Erro interno da Shopee."""