from .category_model import Category
from .establishment_model import Establishment
from sqlalchemy.orm import relationship


Establishment.category = relationship('Category', back_populates='establishments')
Category.establishments = relationship('Establishment', back_populates='category')