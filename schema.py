from graphene import (
  String,
  Schema,
  List,
  Boolean
)
import graphene
from data import cities
from auth import requires_auth, requires_scope

class Query(graphene.ObjectType):
  hello = String(name=String(default_value="stranger"))
  goodbye = String()
  cities = List(String)

  def resolve_hello(root, info, name):
    return f'Hello {name}!'
  
  def resolve_goodbye(root, info):
    return 'See ya!'

  @requires_scope('read:cities')
  @requires_auth
  def resolve_cities(root, info):
    return cities

class AddCity(graphene.Mutation):
  class Arguments:
    name = String()
  
  ok = Boolean()
  city = String()
  
  @requires_scope('create:cities')
  @requires_auth
  def mutate(root, info, name):
    cities.append(name)
    return AddCity(ok=True, city=name)

class Mutation(graphene.ObjectType):
  add_city = AddCity.Field()

schema = Schema(query=Query, mutation=Mutation)