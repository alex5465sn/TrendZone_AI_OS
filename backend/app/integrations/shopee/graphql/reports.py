"""
Queries oficiais
Conversion Reports
"""

CONVERSION_REPORT = """
query ConversionReport(

    $purchaseTimeStart:Int64
    $purchaseTimeEnd:Int64
    $limit:Int
    $scrollId:String

){

    conversionReport(

        purchaseTimeStart:$purchaseTimeStart
        purchaseTimeEnd:$purchaseTimeEnd
        limit:$limit
        scrollId:$scrollId

    ){

        nodes{

            clickTime

            purchaseTime

            conversionId

            totalCommission

            sellerCommission

            shopeeCommissionCapped

            netCommission

            buyerType

            device

            productType

            utmContent

            orders{

                orderId

                shopType

                orderStatus

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

VALIDATED_REPORT = """
query ValidatedReport(

    $validationId:Int64!
    $limit:Int
    $scrollId:String

){

    validatedReport(

        validationId:$validationId
        limit:$limit
        scrollId:$scrollId

    ){

        nodes{

            conversionId

            totalCommission

            sellerCommission

            shopeeCommissionCapped

            netCommission

            buyerType

            device

            productType

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