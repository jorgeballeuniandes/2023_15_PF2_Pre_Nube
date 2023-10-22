from src.commands.create_it_specialist import CreateItSpecialist
from src.session import Session, engine
from src.models.model import Base
from src.models.it_specialist import ItSpecialist
from src.errors.errors import IncompleteParams, InvalidDates
from datetime import datetime, timedelta

class TestCreateItSpecialist():
  def setup_method(self):
    Base.metadata.create_all(engine)
    self.session = Session()

  def test_create_it_specialist(self):
    data = {
      'name': "Juan",
      'email': "Juan@gmail.com",
      'nationality': "Colombia",
      'profession': "Developer",
      'speciality': ".NET Junior Developer",
      'profile': "Great developer"      
    }
    userId = 1
    it_specialist = CreateItSpecialist(data, userId).execute()
    assert it_specialist['userId'] == userId
    assert it_specialist['name'] == data['name']
    assert it_specialist['email'] == data['email']
    assert it_specialist['nationality'] == data['nationality']
    assert it_specialist['profession'] == data['profession']
    assert it_specialist['profile'] == data['profile']
    
  def test_create_it_specialist_missing_fields(self):
    try:
      CreateItSpecialist({}).execute()
      assert False
    except IncompleteParams:
      assert True

  def teardown_method(self):
    self.session.close()
    Base.metadata.drop_all(bind=engine)