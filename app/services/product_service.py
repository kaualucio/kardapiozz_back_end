from uuid import UUID
from app.models.product_model import Product
from app.extensions.db import db
from datetime import datetime

class ProductService:
  @staticmethod
  def create(name: str, image: str, ingredients: list[str], price: float, establishment_id: UUID):
    new_product = Product(name=name, image=image, ingredients=ingredients, price=price, establishment_id=establishment_id)
    db.session.add(new_product)
    db.session.commit()
    return new_product
  
  @staticmethod
  def find_by_id(id: UUID):
    product = db.session.execute(db.select(Product).filter_by(id=id)).scalars().first()
    return product
  
  @staticmethod
  def find_all_by_establishment_id(establishment_id: UUID):
    products = db.session.execute(db.select(Product).filter_by(establishment_id=establishment_id)).scalars().all()
    return products
  
  @staticmethod
  def find_all_by_menu_id(menu_id: UUID):
    products = db.session.execute(db.select(Product).filter_by(menu_id=menu_id)).scalars().all()
    return products
  
  @staticmethod
  def update(id: UUID, **kwargs):
    product = ProductService.find_by_id(id)
    for key, value in kwargs.items():
      setattr(product, key, value)
    
    setattr(product, 'updated_at', datetime.now())
    db.session.commit()
    return product
  
  @staticmethod
  def delete(id: UUID):
    product = ProductService.find_by_id(id)
    db.session.delete(product)
    db.session.commit()
    return product