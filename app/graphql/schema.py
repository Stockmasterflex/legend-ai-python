"""
GraphQL Schema
Main schema combining queries, mutations, and subscriptions
"""

import strawberry
from .queries import Query
from .mutations import Mutation
from .subscriptions import Subscription


# Create the GraphQL schema
schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    subscription=Subscription,
    extensions=[
        # Add extensions for better debugging and performance
    ]
)


# Export schema for use in FastAPI
__all__ = ["schema"]
