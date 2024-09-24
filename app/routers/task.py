from app.types.task import Query,Mutations
from strawberry.fastapi import GraphQLRouter
import strawberry



schema=strawberry.Schema(Query,Mutations)

graphql_app=GraphQLRouter(schema,prefix="/tasks")




