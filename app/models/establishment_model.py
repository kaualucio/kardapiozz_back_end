from typing import Optional, Any
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, String, Text, ForeignKey
from app.extensions.db import db
from uuid import uuid4, UUID
from sqlalchemy.types import JSON
from datetime import datetime, timezone
# from app.models.category_model import Category

class Establishment(db.Model):
  __tablename__ = 'establishment'
  
  type_annotation_map = {
    dict[str, Any]: JSON
  }
  
  id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4, unique=True)
  name: Mapped[str] = mapped_column(String(255), nullable=True)
  slug: Mapped[str] = mapped_column(String(255), nullable=False)
  email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
  about: Mapped[str] = mapped_column(Text(), nullable=True)
  picture: Mapped[str] = mapped_column(Text(), nullable=True)
  address: Mapped[str] = mapped_column(String(255), nullable=True)
  phone: Mapped[str] = mapped_column(String(11), nullable=True, unique=True)
  open_days: Mapped[JSON] = mapped_column(JSON, nullable=True)
  is_active: Mapped[bool] = mapped_column(nullable=False, default=False)
  is_open: Mapped[bool] = mapped_column(nullable=False, default=False)
  is_information_set: Mapped[bool] = mapped_column(nullable=False, default=False)
  created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(tz=timezone.utc))
  updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(tz=timezone.utc))
  
  category_id: Mapped[UUID] = mapped_column(ForeignKey('category.id'), nullable=True, unique=True)

  
  def __init__(
    self, 
    id = None,
    name = None, 
    slug = None, 
    # dashboard_id = None, 
    email = None,
    about = None, 
    picture = None, 
    address = None, 
    phone = None, 
    open_days = None, 
    category_id = None,
    is_active = False,
    is_open = False,
    is_information_set = False,
    ):
    self.id = id
    self.name = name
    self.slug = slug
    self.email = email
    self.about = about
    self.phone = phone
    self.picture = picture
    self.address = address
    self.open_days = open_days
    self.category_id = category_id
    self.is_active = is_active
    self.is_open = is_open
    self.is_information_set = is_information_set

  
  def __repr__(self):
    return f'<Establishment {self.name}, {self.email}, {self.is_active}>'
  
  def to_dict(self):
    return  {
      'id': self.id,
      'email': self.email,
      'name': self.name,
      'slug': self.slug,
      'about': self.about,
      'phone': self.phone,
      'picture': self.picture,
      'address': self.address,
      'open_days': self.open_days,
      'category_id': self.category_id,
      'is_active': self.is_active,
      'is_open': self.is_open,
      'is_information_set': self.is_information_set,
    }
  