from fastapi import Request
from fastapi.responses import JSONResponse


class TrendZoneException(Exception):
    """
    Exceção base do sistema.
    """

    default_message = "Erro interno."

    def __init__(
        self,
        message: str | None = None,
    ):
        self.message = message or self.default_message
        super().__init__(self.message)


# =====================================================
# EXCEPTION HANDLERS
# =====================================================

async def trendzone_exception_handler(
    request: Request,
    exc: TrendZoneException,
):
    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "error": exc.message,
            "type": exc.__class__.__name__,
        },
    )


async def generic_exception_handler(
    request: Request,
    exc: Exception,
):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Erro interno do servidor.",
            "detail": str(exc),
            "type": exc.__class__.__name__,
        },
    )


# =====================================================
# VALIDAÇÃO
# =====================================================

class ValidationException(TrendZoneException):
    default_message = "Erro de validação."


class InvalidPriceException(ValidationException):
    default_message = "Preço inválido."


class InvalidCommissionException(ValidationException):
    default_message = "Comissão inválida."


class InvalidRatingException(ValidationException):
    default_message = "Avaliação inválida."


class InvalidSalesException(ValidationException):
    default_message = "Quantidade de vendas inválida."


# =====================================================
# PRODUTOS
# =====================================================

class ProductException(TrendZoneException):
    default_message = "Erro relacionado ao produto."


class ProductAlreadyExists(ProductException):
    default_message = "Produto já cadastrado."


class ProductNotFound(ProductException):
    default_message = "Produto não encontrado."


# =====================================================
# USUÁRIOS
# =====================================================

class UserException(TrendZoneException):
    default_message = "Erro relacionado ao usuário."


class UserAlreadyExists(UserException):
    default_message = "Usuário já cadastrado."


class UserNotFound(UserException):
    default_message = "Usuário não encontrado."


class InvalidCredentials(UserException):
    default_message = "Credenciais inválidas."


# =====================================================
# AUTENTICAÇÃO
# =====================================================

class AuthenticationException(TrendZoneException):
    default_message = "Falha de autenticação."


class AuthorizationException(TrendZoneException):
    default_message = "Acesso negado."


class InvalidToken(AuthenticationException):
    default_message = "Token inválido."


class ExpiredToken(AuthenticationException):
    default_message = "Token expirado."


# =====================================================
# BANCO
# =====================================================

class DatabaseException(TrendZoneException):
    default_message = "Erro no banco de dados."


# =====================================================
# SYSTEM INFO
# =====================================================

class SystemInfoException(TrendZoneException):
    default_message = "Erro relacionado às informações do sistema."


class SystemInfoNotFound(SystemInfoException):
    default_message = "Informações do sistema não encontradas."


# =====================================================
# PIPELINE
# =====================================================

class PipelineException(TrendZoneException):
    default_message = "Erro no Pipeline."


class ScoutException(PipelineException):
    default_message = "Erro durante o Scout."


class DecisionException(PipelineException):
    default_message = "Erro no Decision Engine."


class ReportException(PipelineException):
    default_message = "Erro na geração do relatório."


# =====================================================
# INTEGRAÇÕES
# =====================================================

class IntegrationException(TrendZoneException):
    default_message = "Erro de integração."


class ShopeeException(IntegrationException):
    default_message = "Erro na integração Shopee."


class MarketplaceUnavailable(IntegrationException):
    default_message = "Marketplace indisponível."