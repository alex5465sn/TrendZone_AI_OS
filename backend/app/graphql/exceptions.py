"""
TrendZone AI OS

GraphQL Exceptions
"""


class GraphQLException(Exception):

    pass


class GraphQLRequestException(GraphQLException):

    pass


class GraphQLResponseException(GraphQLException):

    pass


class GraphQLAuthenticationException(GraphQLException):

    pass