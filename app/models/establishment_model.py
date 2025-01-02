from typing import Any
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.inspection import inspect
from sqlalchemy import DateTime, String, Text, ForeignKey
from app.extensions.db import db
from uuid import uuid4, UUID
from sqlalchemy.types import JSON
from datetime import datetime, timezone

from app.models.menu_model import Menu

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
  # menus: Mapped[list['Menu']] = relationship('Menu', back_populates='establishment')

  
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
  
  def to_dict(self, with_data_relations: bool = False):
    dictionary = { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }
    if with_data_relations:  
      category_dictionary = self.category.to_dict() if self.category else None
      dictionary['category'] = category_dictionary
    return dictionary