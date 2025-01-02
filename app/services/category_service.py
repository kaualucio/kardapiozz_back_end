from uuid import UUID
from datetime import datetime

from app.extensions.db import db
from app.utils.slugfy import slugfy
from app.models.category_model import Category
class CategoryService:
  @staticmethod
  def create(name: str):
    new_categoy = Category(name=name, slug=slugfy(name))
    db.session.add(new_categoy)
    db.session.commit()
    return new_categoy
  
  @staticmethod
  def find_by_id(id: UUID):
    category = db.session.execute(db.select(Category).filter_by(id=id)).scalars().first()
    return category
  
  @staticmethod
  def update(new_name: str):
    category = db.session.execute(db.select(Category).filter_by(id=id)).scalars().first()
    category.name = new_name
    category.slug = slugfy(new_name)
    category.updated_at = datetime.now()
    db.session.commit()
    return category
  
  @staticmethod
  def delete(id: UUID):
    category = db.session.execute(db.select(Category).filter_by(id=id)).scalars().first()
    db.session.delete(category)
    db.session.commit()
    return category