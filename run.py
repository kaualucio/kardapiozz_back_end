from app import create_app
from app.extensions.db import db
from app.models.category_model import Category

app = create_app()
if __name__ == '__main__':
  # TO-DO: IMPLEMENTING CORS
  def seed_db():
    # SEED ALL TYPES/CATEGORYS OF RESTAURANTS
    bar = Category(name='Bar', slug='bar')
    pizza_place = Category(name='Pizzaria', slug='pizzaria')
    burguer_place = Category(name='Hamburgueria', slug='hamburgueria')
    italian = Category(name='Italiano', slug='italiano')
    brazilian = Category(name='Brasileiro', slug='brasileiro')
    japanase = Category(name='Japonês', slug='japones')
    db.session.add_all([bar, pizza_place, burguer_place, italian, brazilian, japanase])
    db.session.commit()
    print('SEED COMPLETED')
  
  
  # with app.app_context():
  #   db.drop_all()
  #   db.create_all()
  #   seed_db()
  app.run(debug=True)