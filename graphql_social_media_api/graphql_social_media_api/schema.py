import graphene
from graphene_django import DjangoObjectType
from graphql_api import models

class User(DjangoObjectType):
    class Meta:
        model = models.User

class UserInput(graphene.InputObjectType):
    name = graphene.String()
    
    
class CreateUser(graphene.Mutation):
    class Arguments:
        input = UserInput(required=True)
        
    ok = graphene.Boolean()
    user = graphene.Field(User)    
    
    @staticmethod
    def mutate(root, info, input):
        instance = models.User(name=input.name)
        
        try:
            instance.save()
        except Exception:
            return CreateUser(ok=False, user=None)
        
        return CreateUser(ok=True, user=instance)
    

class Query(graphene.ObjectType):
    user = graphene.Field(User, id=graphene.Int())
    
    def resolve_user(self, info, **kwargs):
        id = kwargs.get("id")
        
        if id is not None:
            return models.User.objects.get(pk=id)
        
        return None
    

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    
    

schema = graphene.Schema(query=Query, mutation=Mutation)

