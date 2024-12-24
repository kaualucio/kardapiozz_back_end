import os
import dotenv
from datetime import timedelta

dotenv.load_dotenv(override=True)

class Config:
  """Configuração básica"""
  # FLASK
  FLASK_ENV = os.getenv('FLASK_ENV')
  FLASK_DEBUG = os.getenv('FLASK_DEBUG')
  FLASK_PORT = os.getenv('FLASK_PORT')
  FLASK_SECRET = os.getenv('FLASK_SECRET')
  
  # Database and SQLAlchemy
  DATABASE_USERNAME = os.getenv('DATABASE_USERNAME')
  DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
  DATABASE_PORT = os.getenv('DATABASE_PORT')
  DATABASE_HOST = os.getenv('DATABASE_HOST')
  DATABASE_NAME = os.getenv('DATABASE_NAME')
  DATABASE_URI = f'mysql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}'
  SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS') 
  
  # JWT
  JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
  JWT_COOKIE_SECURE = os.environ.get('JWT_COOKIE_SECURE')
  JWT_TOKEN_LOCATION = os.environ.get('JWT_TOKEN_LOCATION')
  JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=60)
  JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
  
  # E-mail
  SEND_MAIL_USER = os.getenv('SEND_MAIL_USER')
  SEND_MAIL_PASS = os.getenv('SEND_MAIL_PASS')
  
  #AWS COGNITO
  REGION_NAME = os.getenv('REGION_NAME')
  COGNITO_CLIENT_ID = os.getenv('COGNITO_CLIENT_ID')
  COGNITO_CLIENT_SECRET = os.getenv('COGNITO_CLIENT_SECRET')
  COGNITO_USER_POOL_ID = os.getenv('COGNITO_USER_POOL_ID')
config = Config()