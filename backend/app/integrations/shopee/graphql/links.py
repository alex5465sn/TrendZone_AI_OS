"""
Mutations oficiais
Short Links
"""

GENERATE_SHORT_LINK = """
mutation GenerateShortLink(

    $originUrl:String!
    $subIds:[String!]

){

    generateShortLink(

        input:{

            originUrl:$originUrl
            subIds:$subIds

        }

    ){

        shortLink

        longLink

    }

}
"""

GENERATE_BATCH_SHORT_LINK = """
mutation GenerateBatchShortLink(

    $links:[GenerateShortLinkInput!]!

){

    generateBatchShortLink(

        input:{

            links:$links

        }

    ){

        total

        successCount

        links{

            originUrl

            shortLink

            longLink

            success

            errorMessage

        }

    }

}
"""