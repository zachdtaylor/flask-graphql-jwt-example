import json

from flask import request, _request_ctx_stack
from functools import wraps
from graphql import GraphQLError
from jose import jwt
from six.moves.urllib.request import urlopen

AUTH0_DOMAIN = 'dev-xy2tjdsq.auth0.com'
API_AUDIENCE = 'https://jwttest/api'
ALGORITHMS = ['RS256']

def get_token_auth_header():
  """Obtains the Access Token from the Authorization Header

  Returns:
    (str): Authorization token from the request
  
  Raises:
    AuthError: If the token header does not exist or is badly formatted
  """
  auth = request.headers.get("Authorization", None)
  if not auth:
    raise GraphQLError("Authorization header is expected")
  
  parts = auth.split()

  if parts[0].lower() != "bearer":
    raise GraphQLError("Authorization header must start with 'Bearer'")
  elif len(parts) == 1:
    raise GraphQLError("Token not found")
  elif len(parts) > 2:
    raise GraphQLError("Authorization header must be 'Bearer token'")

  token = parts[1]
  return token

def requires_auth(f):
  """Determine if the Access Token is valid
  """
  @wraps(f)
  def decorated(*args, **kwargs):
    token = get_token_auth_header()
    # The JSON web key set is at this URL
    jsonurl = urlopen('https://'+AUTH0_DOMAIN+'/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    # base64 decode the header of the JWT
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    for key in jwks["keys"]:
      if key["kid"] == unverified_header["kid"]:
        rsa_key = {
          "kty": key["kty"],
          "kid": key["kid"],
          "use": key["use"],
          "n": key["n"],
          "e": key["e"]
        }
    if rsa_key:
      try:
        payload = jwt.decode(
          token,
          rsa_key,
          algorithms=ALGORITHMS,
          audience=API_AUDIENCE,
          issuer="https://"+AUTH0_DOMAIN+"/"
        )
      except jwt.ExpiredSignatureError:
        raise GraphQLError("Token is expired")
      except jwt.JWTClaimsError:
        raise GraphQLError("Incorrect claims, please check the audience and issuer")
      except Exception:
        raise GraphQLError("Unable to parse authentication token.")
      _request_ctx_stack.top.current_user = payload
      return f(*args, **kwargs)
    raise GraphQLError("Unable to find appropriate key")
  return decorated

def requires_scope(required_scope):
  """Determines if the required scope is present in the Access Token
  
  Parameters:
    required_scope (str): The scope required to access the resource
  """
  def decorator(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
      token = get_token_auth_header()
      unverified_claims = jwt.get_unverified_claims(token)
      if unverified_claims.get("scope"):
        token_scopes = unverified_claims["scope"].split()
        for token_scope in token_scopes:
          if token_scope == required_scope:
            return f(*args, **kwargs)
      return GraphQLError("Access denied: field "+_get_field_name(f)+" requires scope "+required_scope)
    return wrapper
  return decorator

def _get_field_name(f):
  field = ''
  if f.__name__.startswith('resolve'):
    field = f.__name__.split('_')[1]
  elif f.__name__ == 'mutate':
    field = f.__qualname__.split('.')[0]
    field = field[0].lower() + field[1:]
  return field