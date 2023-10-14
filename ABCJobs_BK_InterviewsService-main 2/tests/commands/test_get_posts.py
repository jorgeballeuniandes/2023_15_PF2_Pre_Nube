from src.commands.get_interviews import Getinterviews
from src.commands.create_post import CreateInterview
from src.session import Session, engine
from src.models.model import Base
from src.models.interview import Interview
from src.errors.errors import InvalidParams
from datetime import datetime, timedelta

class TestGetinterviews():
  def setup_method(self):
    Base.metadata.create_all(engine)
    self.session = Session()
    self.post_data = {
      'routeId': 1,
      'plannedStartDate': datetime.now().date().isoformat(),
      'plannedEndDate': (datetime.now() + timedelta(days=2)).date().isoformat()
    }
    self.userId = 1
    self.interview = CreateInterview(self.post_data, self.userId).execute()

  def test_get_interviews(self):
    data = {
      'when': datetime.now().date().isoformat(),
      'route': self.post_data['routeId'],
      'filter': 'me'
    }
    interviews = Getinterviews(data, self.userId).execute()
    assert len(interviews) == 1

    data['when'] = (datetime.now() + timedelta(days=3)).date().isoformat()
    interviews = Getinterviews(data, self.userId).execute()
    assert len(interviews) == 0

  def test_get_interviews_invalid_dates(self):
    try:
      data = {
        'when': 'invalid',
        'route': self.post_data['routeId'],
        'filter': 'me'
      }
      Getinterviews(data, self.userId).execute()
      assert False
    except InvalidParams:
      assert True

  def teardown_method(self):
    self.session.close()
    Base.metadata.drop_all(bind=engine)