import boto3
import botocore.exceptions as exceptions
import hmac
import hashlib
import base64

from ..config import config

class CognitoService:
  def __init__(self):
    self.client = boto3.client('cognito-idp', region_name=config.REGION_NAME)
    
  def _generate_hash_secret(self, username, client_id, client_secret):
    message = username + client_id
    key = bytes(client_secret, 'utf-8')
    secret_hash = base64.b64encode(hmac.new(key, message.encode('utf-8'), hashlib.sha256).digest()).decode()
    return secret_hash
  
  def sign_up(self, establishment_name, email, password):
    try:
      SECRET_HASH = self._generate_hash_secret(email, config.COGNITO_CLIENT_ID, config.COGNITO_CLIENT_SECRET)
      response = self.client.sign_up(
        ClientId=config.COGNITO_CLIENT_ID,
        Username=email,
        Password=password,
        SecretHash=SECRET_HASH,
        UserAttributes=[
          {
            'Name': 'email',
            'Value': email
          },
            {
              'Name': 'given_name',
              'Value': establishment_name
            }
        ]
      )
      return response
    except exceptions.ClientError as error:
      raise error

  def confirm_registration(self, email, confirm_code):
    try:
      SECRET_HASH = self._generate_hash_secret(email, config.COGNITO_CLIENT_ID, config.COGNITO_CLIENT_SECRET)
      self.client.confirm_sign_up(
        ClientId=config.COGNITO_CLIENT_ID,
        Username=email,
        ConfirmationCode= confirm_code,
        SecretHash=SECRET_HASH,
      )
      
      return True
    except exceptions.ClientError as error:
      raise error
  
  def resend_code_confirmation(self, email):
    try:
      self.client.resend_confirmation_code(
        ClientId=config.COGNITO_CLIENT_ID,
        Username=email
      )
      return True
    except exceptions.ClientError as error:
      raise error
  
  def sign_in(self, email, password):
    try:
      SECRET_HASH = self._generate_hash_secret(email, config.COGNITO_CLIENT_ID, config.COGNITO_CLIENT_SECRET)
      response = self.client.initiate_auth(
        ClientId=config.COGNITO_CLIENT_ID,
        AuthFlow='USER_PASSWORD_AUTH',
        # SecretHash=SECRET_HASH,
        AuthParameters={
          'USERNAME': email,
          'PASSWORD': password,
          'SECRET_HASH': SECRET_HASH
        }
      )
      return response['AuthenticationResult']
    except exceptions.ClientError as error:
      raise error
  
  def refresh_token(self, refresh_token_code, establishment_id):
    try:
      SECRET_HASH = self._generate_hash_secret(establishment_id, config.COGNITO_CLIENT_ID, config.COGNITO_CLIENT_SECRET)
      response = self.client.initiate_auth(
        ClientId=config.COGNITO_CLIENT_ID,
        AuthFlow="REFRESH_TOKEN_AUTH",
        AuthParameters={
          'REFRESH_TOKEN': refresh_token_code,
          'SECRET_HASH': SECRET_HASH,
        }
      )
      # print(response)
      return response
    except exceptions.ClientError as error:
      print(error)
      raise error

  def logout(self, access_token, establishment_id):
    try:
      response = self.client.global_sign_out(
        AccessToken=access_token
      )
      return response
    except exceptions.ClientError as error:
      print(error)
      raise error
  
  # def get_user(self, access_token):
  #   try:
  #     SECRET_HASH = self._generate_hash_secret('kauadefreitas.s992@gmail.com', config.COGNITO_CLIENT_ID, config.COGNITO_CLIENT_SECRET)
  #     response = self.client.initiate_auth(
  #       ClientId=config.COGNITO_CLIENT_ID,
  #       AuthFlow='USER_AUTH',
  #       AuthParameters={
  #         'ACCESS_TOKEN': access_token,
  #         'SECRET_HASH': SECRET_HASH
  #       }
  #       # AccessToken=
  #     )
      
  #     return response
  #   except exceptions.ClientError as error:
  #     raise error

cognito_service = CognitoService()