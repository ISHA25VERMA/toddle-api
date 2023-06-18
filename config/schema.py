import auth.schema
import journals.schema
import graphene

class Query(journals.schema.Query,auth.schema.Query, graphene.ObjectType):
    pass

class Mutation(journals.schema.Mutation, auth.schema.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema( mutation=Mutation, query=Query)