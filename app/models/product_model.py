from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.inspection import inspect
from sqlalchemy import DateTime, String,Text, Float, Integer, Boolean, ForeignKey, JSON
from uuid import uuid4, UUID
from typing import Any, Optional
from  datetime import datetime, timezone

from app.extensions.db import db

class Product(db.Model):
  __tablename__ = 'products'
  
  id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4, unique=True)
  name: Mapped[str] = mapped_column(String(100), nullable=False)
  image: Mapped[str] = mapped_column(Text, nullable=False)
  price: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
  ingredients: Mapped[list] = mapped_column(JSON, nullable=False)
  is_available: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
  quantity_purchased: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
  created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(tz=timezone.utc))
  updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(tz=timezone.utc))
  establishment_id: Mapped[UUID] = mapped_column(ForeignKey('establishment.id'))
  menu_id: Mapped[UUID] = mapped_column(ForeignKey('menu.id'), nullable=True)
  
  def __init__(self, name, image, price, ingredients, establishment_id):
    self.name = name
    self.image = image
    self.price = price
    self.ingredients = ingredients
    self.establishment_id = establishment_id
        
  def __repr__(self):
    return f'<Product name={self.name} menu_id={self.menu_id}>'
  
  def to_dict(self, with_data_relations: bool = False):
    dictionary = { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }
    if with_data_relations:  
      menu_dictionary = self.menu.to_dict() if self.menu else None
      dictionary['menu'] = menu_dictionary
    
    return dictionary