from src.commands.get_interviews import GetInterviews
from src.commands.create_interview import CreateInterview
from src.session import Session, engine
from src.models.model import Base
from tests.mocks import mock_it_specialist_found, mock_company_found, mock_project_found
from httmock import HTTMock
from uuid import uuid4
from src.errors.errors import InvalidParams
from datetime import datetime, timedelta

class TestGetinterviews():
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

  def test_get_interviews(self):
    interviews = GetInterviews().execute()
    assert len(interviews) == 1

  def teardown_method(self):
    self.session.close()
    Base.metadata.drop_all(bind=engine)