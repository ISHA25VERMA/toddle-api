import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from .models import Journal, Tags

class JournalType(SQLAlchemyObjectType):
    pk = graphene.Int(source='id')
    class Meta:
        model = Journal
        interfaces = (graphene.relay.Node, )

class TagsType(SQLAlchemyObjectType):
    pk = graphene.Int(source='id')
    class Meta:
        model = Tags
        interfaces = (graphene.relay.Node, )