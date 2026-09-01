"""
Queries oficiais da Shopee Affiliate API
Product Offer V2
"""


PRODUCT_OFFER_V2 = """
query ProductOfferV2(

    $listType:Int
    $matchId:Int64
    $keyword:String
    $sortType:Int
    $page:Int
    $limit:Int
    $itemId:Int64
    $shopId:Int64
    $productCatId:Int
    $isAMSOffer:Boolean
    $isKeySeller:Boolean

){

    productOfferV2(

        listType:$listType
        matchId:$matchId
        keyword:$keyword
        sortType:$sortType
        page:$page
        limit:$limit
        itemId:$itemId
        shopId:$shopId
        productCatId:$productCatId
        isAMSOffer:$isAMSOffer
        isKeySeller:$isKeySeller

    ){

        nodes{

            itemId

            productName

            shopName

            shopId

            productLink

            offerLink

            imageUrl

            price

            priceMin

            priceMax

            sales

            commission

            commissionRate

            sellerCommissionRate

            shopeeCommissionRate

            appExistRate

            appNewRate

            webExistRate

            webNewRate

            ratingStar

            priceDiscountRate

            productCatIds

            shopType

            periodStartTime

            periodEndTime

        }

        pageInfo{

            page

            limit

            hasNextPage

            scrollId

        }

    }

}
"""