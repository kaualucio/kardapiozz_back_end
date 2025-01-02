from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_migrate import Migrate
from .config import config
from app.extensions.db import db

def create_app(testing_mode=None):
  app = Flask(__name__)
  if testing_mode == True:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
  else:
      app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URI
  app.config['DEBUG'] = config.FLASK_DEBUG
  app.config['MYSQL_HOST'] = config.DATABASE_HOST
  app.config['MYSQL_USER'] = config.DATABASE_USERNAME
  app.config['MYSQL_PASSWORD'] = config.DATABASE_PASSWORD
  app.config['MYSQL_DB'] = config.DATABASE_NAME
  app.config['MYSQL_PORT'] = config.DATABASE_PORT
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.SQLALCHEMY_TRACK_MODIFICATIONS
  app.config['JWT_SECRET_KEY'] = config.JWT_SECRET_KEY
  app.config['JWT_ACCESS_TOKEN_EXPIRES'] = config.JWT_ACCESS_TOKEN_EXPIRES
  app.config['JWT_REFRESH_TOKEN_EXPIRES'] = config.JWT_REFRESH_TOKEN_EXPIRES
  app.config['JWT_TOKEN_LOCATION'] = config.JWT_TOKEN_LOCATION
  app.config['JWT_COOKIE_SECURE'] = config.JWT_COOKIE_SECURE
  app.config['SECRET_KEY'] = config.FLASK_SECRET
  
  # Init Database
  db.init_app(app)
  # Flask Migrate 
  migrate = Migrate(app, db)
  # Register blueprints
  from .routes.auth_routes import auth as auth_blueprint
  from .routes.establishment_routes import establishment as establishment_blueprint
  from .routes.menu_routes import menu as menu_blueprint
  from .routes.product_routes import product as product_blueprint
  app.register_blueprint(auth_blueprint, url_prefix="/auth")
  app.register_blueprint(establishment_blueprint, url_prefix="/establishment")
  app.register_blueprint(menu_blueprint, url_prefix="/menu")
  app.register_blueprint(product_blueprint, url_prefix="/product")
  
  return app