import pytest
from app import create_app
from app.extensions.db import db

@pytest.fixture(scope='module')
def client():
  app = create_app(testing_mode=True)
  # app.config['TESTING'] = True
  # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
  # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  with app.test_client() as client:
    with app.app_context():
      db.create_all()
      yield client
      with app.app_context():
        db.drop_all()