"""
Queries oficiais
Item Feed
"""

LIST_ITEM_FEEDS = """
query{

    listItemFeeds{

        feeds{

            datafeedId

            referenceId

            datafeedName

            description

            totalCount

            grassDate

            feedMode

        }

    }

}
"""

GET_ITEM_FEED_DATA = """
query GetItemFeedData(

    $datafeedId:String!
    $offset:Int
    $limit:Int

){

    getItemFeedData(

        datafeedId:$datafeedId
        offset:$offset
        limit:$limit

    ){

        rows{

            columns

            updateType

        }

        pageInfo{

            offset

            limit

            totalCount

            hasMore

        }

    }

}
"""