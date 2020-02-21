from flask import Flask, jsonify 
from flask_graphql import GraphQLView
from schema import schema
from models import init_db

app = Flask(__name__)

# Add graphql endpoint
app.add_url_rule(
  '/graphql',
  view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True)
)

if __name__ == '__main__':
  init_db()
  app.run(host='0.0.0.0', debug=True)