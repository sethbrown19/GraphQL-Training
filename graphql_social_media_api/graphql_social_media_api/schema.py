import graphene
from graphene_django import DjangoObjectType
from graphql_api import models

class User(DjangoObjectType):
    class Meta:
        model = models.User


class Query(graphene.ObjectType):
    user = graphene.Field(User, id=graphene.Int())

schema = graphene.Schema(query=Query)