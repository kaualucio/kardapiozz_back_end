from uuid import UUID
from app.extensions.db import db
from app.models.establishment_model import Establishment
from datetime import datetime
class EstablishmentService:
  @staticmethod
  def create_establishment(id: UUID, email: str, establishment_name: str, slug: str, is_active: bool = False):
    new_establishment = Establishment(id=id, email=email, name=establishment_name, slug=slug, is_active=is_active)
    db.session.add(new_establishment)
    db.session.commit()
    return new_establishment
  
  @staticmethod
  def update_establishment(id: UUID, **kwargs):
    # establishment = db.session.execute(db.select(Establishment).filter_by(id=id)).scalars().first()
    establishment = EstablishmentService.get_by_id(id)
    for key, value in kwargs.items():
      if key == 'category_id':
        setattr(establishment, key, UUID(value))
        continue
      setattr(establishment, key, value)
    setattr(establishment, 'updated_at', datetime.now())
    db.session.commit()
    return establishment
  
  @staticmethod
  def activate_establishment(email: str,):
    establishment = db.session.execute(db.select(Establishment).filter_by(email=email)).scalars().first()
    establishment.is_active = True
    db.session.commit()
    return establishment
  
  @staticmethod
  def get_by_id(id: UUID):
    establishment = db.session.execute(db.select(Establishment).filter_by(id=id)).scalars().first()
    return establishment
  
  @staticmethod
  def get_active_by_id(id: UUID):
    establishment = db.session.execute(db.select(Establishment).filter_by(id=id, is_active=True)).scalars().first()
    return establishment
  
  @staticmethod
  def get_by_email(email: str):
    establishment = db.session.execute(db.select(Establishment).filter_by(email=email)).scalars().first()
    return establishment
    
    