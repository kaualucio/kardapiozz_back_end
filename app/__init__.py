from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from .config import config
from app.extensions.db import db

def create_app():
  app = Flask(__name__)
  app.config['DEBUG'] = config.FLASK_DEBUG
  app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URI
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.SQLALCHEMY_TRACK_MODIFICATIONS
  app.config['JWT_SECRET_KEY'] = config.JWT_SECRET_KEY
  app.config['JWT_ACCESS_TOKEN_EXPIRES'] = config.JWT_ACCESS_TOKEN_EXPIRES
  app.config['JWT_REFRESH_TOKEN_EXPIRES'] = config.JWT_REFRESH_TOKEN_EXPIRES
  app.config['JWT_TOKEN_LOCATION'] = config.JWT_TOKEN_LOCATION
  app.config['JWT_COOKIE_SECURE'] = config.JWT_COOKIE_SECURE
  app.config['SECRET_KEY'] = config.FLASK_SECRET
  
  # Init Database
  db.init_app(app)
  
  # Register blueprints
  from .routes.auth_routes import auth as auth_blueprint
  app.register_blueprint(auth_blueprint, url_prefix="/auth")
  from .routes.establishment_routes import establishment as establishment_blueprint
  app.register_blueprint(establishment_blueprint, url_prefix="/establishment")
  
  
  return app