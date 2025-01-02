from sqlalchemy.orm import Mapped, relationship
from .category_model import Category
from .establishment_model import Establishment
from .menu_model import Menu
from .product_model import Product


Establishment.category = relationship('Category', uselist=False, back_populates='establishments')
Category.establishments = relationship('Establishment', back_populates='category')
Establishment.menus = relationship('Menu', back_populates='establishment')
Menu.establishment = relationship('Establishment', uselist=False, back_populates='menus')
Menu.products = relationship('Product', back_populates='menu')
Product.menu = relationship('Menu', uselist=False, back_populates='products')
