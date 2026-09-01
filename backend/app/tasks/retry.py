"""
TrendZone AI OS
================================

Retry Policy

Responsável por repetir
operações que falharam.

Versão Enterprise.
"""

import time

from app.core.logger import TZLogger


class RetryPolicy:

    def __init__(

        self,

        retries: int = 3,

        delay: int = 2,

    ):

        self.retries = retries

        self.delay = delay

    def execute(self, function, *args, **kwargs):

        last_exception = None

        for attempt in range(

            1,

            self.retries + 1,

        ):

            try:

                return function(

                    *args,

                    **kwargs,

                )

            except Exception as e:

                last_exception = e

                TZLogger.warning(

                    "RETRY",

                    f"Tentativa {attempt}/{self.retries} falhou."

                )

                if attempt < self.retries:

                    time.sleep(self.delay)

        TZLogger.error(

            "RETRY",

            "Número máximo de tentativas atingido."

        )

        raise last_exception