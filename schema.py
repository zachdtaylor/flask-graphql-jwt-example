import graphene

from auth import requires_auth, requires_scope
from graphene import relay
from graphene_mongo import MongoengineObjectType
from models import Painting, Product, Brush
import graphene_mongo


class PaintingType(MongoengineObjectType):
  class Meta:
    model = Painting

class BrushType(MongoengineObjectType):
  class Meta:
    model = Brush

class PaintingConnection(relay.Connection):
  class Meta:
    node = PaintingType

class SearchResult(graphene.Union):
  class Meta:
    types = (PaintingType, BrushType)

class Query(graphene.ObjectType):
  search = graphene.List(SearchResult, q=graphene.String())
  paintings = relay.ConnectionField(
    PaintingConnection,
    description="Return all paintings"
  )

  def resolve_paintings(self, info, **args):
    return Painting.objects.all()

  def resolve_search(self, info, q, **args):
    return Product.objects(name__icontains=q)



class PaintingInput(graphene.InputObjectType):
  name = graphene.String(required=True)
  price = graphene.Float(required=True)
  material = graphene.String()
  length = graphene.Float()
  length_uom = graphene.String()
  width = graphene.Float()
  width_uom = graphene.String()

class AddPainting(graphene.Mutation):
  class Arguments:
    data = PaintingInput(required=True)
  
  ok = graphene.Boolean()

  def mutate(self, info, data):
    painting = Painting(**dict(data))
    painting.save()
    return AddPainting(ok=True)

class Mutation(graphene.ObjectType):
  add_painting = AddPainting.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)