from src.commands.get_post import GetItSpecialist
from src.commands.create_post import CreateItSpecialist
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
      'routeId': 1,
      'plannedStartDate': datetime.now().date().isoformat(),
      'plannedEndDate': (datetime.now() + timedelta(days=2)).date().isoformat()
    }
    userId = 1
    self.it_specialist = CreateItSpecialist(data, userId).execute()

  def test_get_post(self):
    it_specialist = GetItSpecialist(self.it_specialist['id']).execute()

    assert it_specialist['id'] == self.it_specialist['id']
    assert it_specialist['userId'] == self.it_specialist['userId']
    assert it_specialist['plannedStartDate'] == self.it_specialist['plannedStartDate']
    assert it_specialist['plannedEndDate'] == self.it_specialist['plannedEndDate']

  def test_get_post_invalid_id(self):
    try:
      GetItSpecialist('Invalid').execute()
      assert False
    except InvalidParams:
      assert True

  def test_get_post_doesnt_exist(self):
    try:
      GetItSpecialist(self.it_specialist['id'] + 1).execute()
      assert False
    except ItSpecialistNotFoundError:
      assert True

  def teardown_method(self):
    self.session.close()
    Base.metadata.drop_all(bind=engine)