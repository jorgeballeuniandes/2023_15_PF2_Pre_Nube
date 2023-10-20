from src.commands.create_interview import CreateInterview
from src.session import Session, engine
from src.models.model import Base
from src.errors.errors import IncompleteParams, ParentNotFoundError
from datetime import datetime, timedelta
from tests.mocks import mock_it_specialist_found, mock_it_specialist_not_found, mock_company_found, mock_company_not_found, mock_project_found, mock_project_not_found
from httmock import HTTMock
from uuid import uuid4

class TestCreateInterview():
  def setup_method(self):
    Base.metadata.create_all(engine)
    self.session = Session()

  def test_create_interview(self):
    with HTTMock(mock_project_found,mock_it_specialist_found, mock_company_found):
      data = {
        "itSpecialistId": 1.0,
        "companyId": 1.0,
        "projectId": 1.0,
        "date": (datetime.now() + timedelta(days=2)).isoformat()
      }
      interview = CreateInterview(data, uuid4()).execute()

      assert 'id' in interview
      assert 'itSpecialistId' in interview
      assert 'companyId' in interview
      assert 'projectId' in interview
      assert 'date' in interview

  def test_create_interview_missing_fields(self):
    with HTTMock(mock_project_found,mock_it_specialist_found, mock_company_found):
      try:
        CreateInterview({},uuid4()).execute()
        assert False
      except IncompleteParams:
        assert True

  def test_create_interview_invalid_it_specialist(self):
    with HTTMock(mock_it_specialist_not_found):
      try:
        data = {
            "itSpecialistId": 1.0,
            "companyId": 1.0,
            "projectId": 1.0,
            "date": (datetime.now() + timedelta(days=2)).isoformat()
          }
        interview = CreateInterview(data, uuid4()).execute()
      except ParentNotFoundError:
        assert True

  def test_create_interview_invalid_company(self):
    with HTTMock(mock_it_specialist_found, mock_company_not_found):
      try:
        data = {
            "itSpecialistId": 1.0,
            "companyId": 1.0,
            "projectId": 1.0,
            "date": (datetime.now() + timedelta(days=2)).isoformat()
          }
        interview = CreateInterview(data, uuid4()).execute()
      except ParentNotFoundError:
        assert True

  def test_create_interview_invalid_project(self):
    with HTTMock(mock_it_specialist_found, mock_company_found, mock_project_not_found):
      try:
        data = {
            "itSpecialistId": 1.0,
            "companyId": 1.0,
            "projectId": 1.0,
            "date": (datetime.now() + timedelta(days=2)).isoformat()
          }
        interview = CreateInterview(data, uuid4()).execute()
      except ParentNotFoundError:
        assert True


  def teardown_method(self):
    self.session.close()
    Base.metadata.drop_all(bind=engine)