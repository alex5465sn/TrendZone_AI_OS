class ProductMapper:

    @staticmethod
    def from_shopee(product: dict) -> dict:

        return {

            "item_id": product["itemId"],

            "shop_id": product["shopId"],

            "name": product["productName"],

            "price": product["price"],

            "commission": product["commissionRate"],

            "rating": product["ratingStar"],

            "sales": product["sales"],

            "image": product["imageUrl"],

            "offer_link": product["offerLink"],

            "active": True,
        }