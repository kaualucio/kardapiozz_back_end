import requests
from app.config import Config
from jose import jwt
from jose.jwk import construct
from functools import wraps
from flask import request, jsonify

def get_jwks():
  jwks_url = f'https://cognito-idp.{Config.REGION_NAME}.amazonaws.com/{Config.COGNITO_USER_POOL_ID}/.well-known/jwks.json'
  response = requests.get(jwks_url)
  return response.json()

def verify_jwt(token):
  jwks = get_jwks()
  headers = jwt.get_unverified_header(token)
  
  kid = headers['kid']
  
  public_key = None
  for key in jwks['keys']:
    if key['kid'] == kid:
      public_key = construct(key)
      break
  if not public_key:
    raise Exception('Public Key not found')

  try:
    payload = jwt.decode(token, public_key, algorithms=['RS256'], audience=Config.COGNITO_CLIENT_ID)
    return payload
  except jwt.ExpiredSignatureError:
    raise Exception('Token has expired.')
  except jwt.JWTClaimsError:
    raise Exception('Incorrect claims, please check the audience and issuer.')
  except Exception as e:
    raise Exception(f"Unable to parse authentication token: {str(e)}")
  
def private_route():
  def decorator(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
      token = request.headers.get('Authorization')
      if not token:
        return jsonify({ 'message': 'Token is missing!' }), 401
      try:
        access_token = token.split(' ')[1]
        payload = verify_jwt(access_token)
        request.user = payload
      except Exception as e:
        print(type(e))
        print('[VERIFY_JWT_DECORATOR_ERROR]', str(e))
        return jsonify({"message": str(e)}), 401 
      
      return f(*args, **kwargs)
    return decorated_function
  return decorator