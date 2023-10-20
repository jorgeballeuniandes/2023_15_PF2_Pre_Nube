from src.commands.validate_it_specialist import ValidateItSpecialist
from httmock import HTTMock
from src.errors.errors import ParentNotFoundError
from uuid import uuid4
from tests.mocks import mock_it_specialist_found, mock_it_specialist_not_found

class TestValidateItSpecialist():
  def test_validate_it_specialist(self):
    with HTTMock(mock_it_specialist_found):
      result = ValidateItSpecialist(1,uuid4()).execute()
      assert 'id' in result

  def test_failed_validate_it_specialist(self):
    with HTTMock(mock_it_specialist_not_found):
      try:
        result = ValidateItSpecialist(1,uuid4()).execute()
        assert False
      except ParentNotFoundError:
        assert True