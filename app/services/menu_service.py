from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional
from app.extensions.db import db
from app.models.menu_model import Menu
from app.services.product_service import ProductService

class MenuService:
  @staticmethod
  def create(name: str, products: Optional[str], establishment_id: UUID, is_active:Optional[bool] = False):
    new_menu = Menu(id=uuid4(), name=name, establishment_id=establishment_id, is_active=is_active)
    db.session.add(new_menu)
    db.session.commit()
    if len(products) > 0:
      for product_id in products:
        MenuService.add_product_to_menu(menu_id=new_menu.id, product_id=UUID(product_id))
    
    return new_menu
  
  def find_menu_by_id(id: UUID, establishment_id: UUID):
    menu = db.session.execute(db.select(Menu).filter_by(id=id, establishment_id=establishment_id)).scalars().first()
    return menu
  
  def find_all_menus_by_establishment_id(establishment_id: UUID):
    menus = db.session.execute(db.select(Menu).filter_by(establishment_id=establishment_id)).scalars().all()  
    return menus
  
  def add_product_to_menu(menu_id: UUID, product_id: UUID):
    product = ProductService.find_by_id(id=product_id)
    if not product:
      return False
    product.menu_id = menu_id
    db.session.commit()
    return True
  
  def update(menu_id: UUID, establishment_id: UUID, **kwargs):
    menu = MenuService.find_menu_by_id(id=menu_id, establishment_id=establishment_id)
    for key, value in kwargs.items():
      if key == 'products' and len(value) > 0:
        for product_id in value:
          MenuService.add_product_to_menu(menu_id=menu_id, product_id=UUID(product_id))
        continue
      setattr(menu, key, value)
    setattr(menu, 'updated_at', datetime.now())
    db.session.commit()
    return menu
  
  def delete(menu_id: UUID, establishment_id: UUID):
    menu = MenuService.find_menu_by_id(id=menu_id, establishment_id=establishment_id)
    if len(menu.products) > 0:
      for product in menu.products:
        ProductService.update(id=product.id, menu_id=None)

    db.session.delete(menu)
    db.session.commit()
    return menu
  