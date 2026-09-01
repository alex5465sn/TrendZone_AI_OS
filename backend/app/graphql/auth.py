"""
TrendZone AI OS
================================

Shopee Authentication
"""

from app.core.settings import settings


class ShopeeAuth:

    @staticmethod
    def headers():

        return {

            "Content-Type": "application/json",

            "Authorization": f"Bearer {settings.SHOPEE_TOKEN}",

            "x-app-id": settings.SHOPEE_APP_ID,

        }