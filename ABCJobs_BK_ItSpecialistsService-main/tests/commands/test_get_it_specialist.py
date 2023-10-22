from src.commands.get_it_specialist import GetItSpecialist
from src.commands.create_it_specialist import CreateItSpecialist
from src.session import Session, engine
from src.models.model import Base
from src.models.it_specialist import ItSpecialist
from src.errors.errors import InvalidParams, ItSpecialistNotFoundError
from datetime import datetime, timedelta

class TestGetItSpecialist():
  def setup_method(self):
    Base.metadata.create_all(engine)
    self.session = Session()

    data = {
              "userId":1,
              "name":"juan",
              "email":"juan@gmail.com",
              "nationality":"Colombia",
              "profession":"Developer",
              "speciality":".NET Junior Developer",
              "profile":"Great developer"
    }
    userId = 1
    self.it_specialist = CreateItSpecialist(data, userId).execute()

  def test_get_it_specialist(self):
    it_specialist = GetItSpecialist(self.it_specialist['id']).execute()

    assert it_specialist['id'] == self.it_specialist['id']
    assert it_specialist['userId'] == self.it_specialist['userId']
    assert it_specialist['name'] == self.it_specialist['name']
    assert it_specialist['email'] == self.it_specialist['email']
    assert it_specialist['nationality'] == self.it_specialist['nationality']
    assert it_specialist['profession'] == self.it_specialist['profession']
    assert it_specialist['speciality'] == self.it_specialist['speciality']
    assert it_specialist['profile'] == self.it_specialist['profile']

  def test_get_it_specialist_invalid_id(self):
    try:
      GetItSpecialist('Invalid').execute()
      assert False
    except InvalidParams:
      assert True

  def test_get_it_specialist_doesnt_exist(self):
    try:
      GetItSpecialist(self.it_specialist['id'] + 1).execute()
      assert False
    except ItSpecialistNotFoundError:
      assert True

  def teardown_method(self):
    self.session.close()
    Base.metadata.drop_all(bind=engine)