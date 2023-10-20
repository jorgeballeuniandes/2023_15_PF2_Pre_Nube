from src.commands.validate_company import ValidateCompany
from httmock import HTTMock
from src.errors.errors import ParentNotFoundError
from uuid import uuid4
from tests.mocks import mock_company_found, mock_company_not_found

class TestValidateCompany():
  def test_validate_company(self):
    with HTTMock(mock_company_found):
      result = ValidateCompany(1,uuid4()).execute()
      assert 'id' in result

  def test_failed_validate_company(self):
    with HTTMock(mock_company_not_found):
      try:
        result = ValidateCompany(1,uuid4()).execute()
        assert False
      except ParentNotFoundError:
        assert True