from src.commands.get_it_specialists import Getit_specialists
from src.commands.create_post import CreateItSpecialist
from src.session import Session, engine
from src.models.model import Base
from src.models.it_specialist import ItSpecialist
from src.errors.errors import InvalidParams
from datetime import datetime, timedelta

class TestGetit_specialists():
  def setup_method(self):
    Base.metadata.create_all(engine)
    self.session = Session()
    self.post_data = {
      'routeId': 1,
      'plannedStartDate': datetime.now().date().isoformat(),
      'plannedEndDate': (datetime.now() + timedelta(days=2)).date().isoformat()
    }
    self.userId = 1
    self.it_specialist = CreateItSpecialist(self.post_data, self.userId).execute()

  def test_get_it_specialists(self):
    data = {
      'when': datetime.now().date().isoformat(),
      'route': self.post_data['routeId'],
      'filter': 'me'
    }
    it_specialists = Getit_specialists(data, self.userId).execute()
    assert len(it_specialists) == 1

    data['when'] = (datetime.now() + timedelta(days=3)).date().isoformat()
    it_specialists = Getit_specialists(data, self.userId).execute()
    assert len(it_specialists) == 0

  def test_get_it_specialists_invalid_dates(self):
    try:
      data = {
        'when': 'invalid',
        'route': self.post_data['routeId'],
        'filter': 'me'
      }
      Getit_specialists(data, self.userId).execute()
      assert False
    except InvalidParams:
      assert True

  def teardown_method(self):
    self.session.close()
    Base.metadata.drop_all(bind=engine)