from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.declarative import declarative_base

class Base(DeclarativeBase):
  pass

# Base = declarative_base()
db = SQLAlchemy(model_class=Base)

class BaseModel(Base):
  __abstract__ = True
    