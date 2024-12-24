from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, String
from app.extensions.db import db
from uuid import uuid4, UUID
from datetime import datetime, timezone
from typing import List

# from app.models.establishment_model import Establishment


class Category(db.Model):
  __tablename__ = 'category'
  
  id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4, nullable=False, unique=True)
  name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
  slug: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
  created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(tz=timezone.utc))
  updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(tz=timezone.utc)) 
  
  # establishments: Mapped[List['Establishment']] = relationship()
  
  def __init__(self, name, slug):
    self.name = name
    self.slug = slug
  
  def __repr__(self):
    return f'<Category {self.name}>'