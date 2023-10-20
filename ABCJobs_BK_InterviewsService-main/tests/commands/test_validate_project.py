from src.commands.validate_project import ValidateProject
from httmock import HTTMock
from src.errors.errors import ParentNotFoundError
from uuid import uuid4
from tests.mocks import mock_project_found, mock_project_not_found

class TestValidateProject():
  def test_validate_project(self):
    with HTTMock(mock_project_found):
      result = ValidateProject(1,uuid4()).execute()
      assert 'id' in result

  def test_failed_validate_project(self):
    with HTTMock(mock_project_not_found):
      try:
        result = ValidateProject(1,uuid4()).execute()
        assert False
      except ParentNotFoundError:
        assert True