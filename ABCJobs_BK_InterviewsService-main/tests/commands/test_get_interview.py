from src.commands.get_interview import GetInterview
from src.commands.create_interview import CreateInterview
from src.session import Session, engine
from src.models.model import Base
from src.errors.errors import InvalidParams, InterviewNotFoundError
from datetime import datetime, timedelta
from tests.mocks import mock_it_specialist_found, mock_company_found, mock_project_found
from httmock import HTTMock
from uuid import uuid4

class TestGetInterview():
  def setup_method(self):
    Base.metadata.create_all(engine)
    self.session = Session()
    with HTTMock(mock_project_found,mock_it_specialist_found, mock_company_found):
      data = {
        "itSpecialistId": 1.0,
        "companyId": 1.0,
        "projectId": 1.0,
        "date": (datetime.now() + timedelta(days=2)).isoformat()
      }
      self.interview = CreateInterview(data, uuid4()).execute()

  def test_get_interview(self):
    interview = GetInterview(self.interview['id']).execute()

    assert interview['id'] == self.interview['id']
    assert interview['itSpecialistId'] == self.interview['itSpecialistId']
    assert interview['companyId'] == self.interview['companyId']
    assert interview['projectId'] == self.interview['projectId']
    assert interview['date'] == self.interview['date']

  def test_get_interview_invalid_id(self):
    try:
      GetInterview('Invalid').execute()
      assert False
    except InvalidParams:
      assert True

  def test_get_interview_doesnt_exist(self):
    try:
      GetInterview(self.interview['id'] + 1).execute()
      assert False
    except InterviewNotFoundError:
      assert True

  def teardown_method(self):
    self.session.close()
    Base.metadata.drop_all(bind=engine)