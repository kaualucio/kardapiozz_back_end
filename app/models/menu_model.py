from typing import Any
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.inspection import inspect
from sqlalchemy import DateTime, String, Text, ForeignKey
from app.extensions.db import db
from uuid import uuid4, UUID
from sqlalchemy.types import JSON
from datetime import datetime, timezone

class Menu(db.Model):
  __tablename__ = 'menu'
  
  type_annotation_map = {
    dict[str, Any]: JSON
  }
  
  id: Mapped[UUID] = mapped_column(primary_key=True, unique=True, nullable=False, default=uuid4)
  name: Mapped[str] = mapped_column(String(100))
  is_active: Mapped[bool] = mapped_column(default=False)
  created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(tz=timezone.utc))
  updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(tz=timezone.utc))
  establishment_id: Mapped[UUID] = mapped_column(ForeignKey('establishment.id'))
  
  def __init__(self, name, establishment_id, id, is_active):
    self.id = id
    self.name = name
    self.is_active = is_active
    self.establishment_id = establishment_id
  
  def __repr__(self):
    return f'<Menu name={self.name} establishment_id={self.establishment_id} is_active={self.is_active}>'
  
  def to_dict(self, with_data_relations: bool = False):
    dictionary = { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }
    if with_data_relations:
      print('with_data_relations', with_data_relations)
      dictionary_products = [product.to_dict() for product in self.products]
      dictionary['products'] = dictionary_products
    return dictionary
  