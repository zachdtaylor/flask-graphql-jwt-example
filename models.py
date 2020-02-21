from mongoengine import Document, fields
from mongoengine import connect

def init_db():
  connect('madelyn-db')

class Product(Document):
  price = fields.DecimalField(precision=2, required=True)
  name = fields.StringField(required=True)
  meta = {'allow_inheritance': True}

class Painting(Product):
  material = fields.StringField()
  length = fields.DecimalField(precision=5)
  length_uom = fields.StringField()
  width = fields.DecimalField(precision=5)
  width_uom = fields.StringField()

class Brush(Product):
  bristle_length = fields.DecimalField(precision=5)
  bristle_length_uom = fields.StringField()
  bristle_density = fields.StringField()

class User(Document):
  email = fields.EmailField()
  name = fields.StringField()