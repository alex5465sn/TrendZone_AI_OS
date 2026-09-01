"""
Queries oficiais da Shopee Affiliate API
Campaigns
"""


SHOP_OFFER_V2 = """
query ShopOfferV2(

    $keyword:String
    $shopType:[Int!]
    $sortType:Int
    $sellerCommCoveRatio:String
    $page:Int
    $limit:Int
    $shopId:Int64
    $isKeySeller:Boolean

){

    shopOfferV2(

        keyword:$keyword
        shopType:$shopType
        sortType:$sortType
        sellerCommCoveRatio:$sellerCommCoveRatio
        page:$page
        limit:$limit
        shopId:$shopId
        isKeySeller:$isKeySeller

    ){

        nodes{

            shopId

            shopName

            imageUrl

            offerLink

            originalLink

            commissionRate

            ratingStar

            periodStartTime

            periodEndTime

            sellerCommCoveRatio

            remainingBudget

            shopType

            bannerInfo{

                count

                banners{

                    fileName

                    imageHeight

                    imageWidth

                    imageSize

                    imageUrl

                }

            }

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


SHOPEE_OFFER_V2 = """
query ShopeeOfferV2(

    $keyword:String
    $sortType:Int
    $page:Int
    $limit:Int

){

    shopeeOfferV2(

        keyword:$keyword
        sortType:$sortType
        page:$page
        limit:$limit

    ){

        nodes{

            offerName

            offerType

            categoryId

            collectionId

            commissionRate

            imageUrl

            offerLink

            originalLink

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