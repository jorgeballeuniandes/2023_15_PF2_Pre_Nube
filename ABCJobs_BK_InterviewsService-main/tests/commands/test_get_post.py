from src.commands.get_post import GetInterview
from src.commands.create_post import CreateInterview
from src.session import Session, engine
from src.models.model import Base
from src.models.interview import Interview
from src.errors.errors import InvalidParams, InterviewNotFoundError
from datetime import datetime, timedelta

class TestGetInterview():
  def setup_method(self):
    Base.metadata.create_all(engine)
    self.session = Session()

    data = {
      'routeId': 1,
      'plannedStartDate': datetime.now().date().isoformat(),
      'plannedEndDate': (datetime.now() + timedelta(days=2)).date().isoformat()
    }
    userId = 1
    self.interview = CreateInterview(data, userId).execute()

  def test_get_post(self):
    interview = GetInterview(self.interview['id']).execute()

    assert interview['id'] == self.interview['id']
    assert interview['userId'] == self.interview['userId']
    assert interview['plannedStartDate'] == self.interview['plannedStartDate']
    assert interview['plannedEndDate'] == self.interview['plannedEndDate']

  def test_get_post_invalid_id(self):
    try:
      GetInterview('Invalid').execute()
      assert False
    except InvalidParams:
      assert True

  def test_get_post_doesnt_exist(self):
    try:
      GetInterview(self.interview['id'] + 1).execute()
      assert False
    except InterviewNotFoundError:
      assert True

  def teardown_method(self):
    self.session.close()
    Base.metadata.drop_all(bind=engine)