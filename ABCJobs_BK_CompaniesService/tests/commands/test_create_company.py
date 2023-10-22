from src.commands.create_company import CreateCompany
from src.session import Session, engine
from src.models.model import Base
from src.errors.errors import IncompleteParams
from tests.mocks import mock_update_companyid
from httmock import HTTMock
from uuid import uuid4

from faker import Faker

class TestCreateCompany():
  def setup_method(self):
    Base.metadata.create_all(engine)
    self.session = Session()

  def test_create_company(self):
    with HTTMock(mock_update_companyid):
      fake = Faker()
      data = {
        'name': fake.name(),
        'email': 'Test Email',
        'address': 'Test Address',
        'country': 'Test Country',
        'dept': 'Test Dept',
        'city': 'Test City',
        'phone': 1234567,
        'contact_name': 'Test Contact Name',
        'contact_phone': 1234567
      }

      company = CreateCompany(data, uuid4(), 2).execute()

      assert 'companyId' in company
      assert 'name' in company
      assert 'email' in company

  def test_create_company_with_incomplete_params(self):
    with HTTMock(mock_update_companyid):
      fake = Faker()
      data = {
        'name': fake.name(),
        'email': 'Test Email',
        'address': 'Test Address',
        'country': 'Test Country',
        'dept': 'Test Dept',
        'city': 'Test City',
        'phone': 1234567,
        'contact_name': 'Test Contact Name',
        'contact_phone': 1234567
      }

      try:
        company = CreateCompany(data, uuid4(), None).execute()
      except IncompleteParams as err:
        assert err.message == 'Missing params: userId'

  def test_create_company_company_already_exists(self):
    with HTTMock(mock_update_companyid):
      fake = Faker()
      data = {
        'name': fake.name(),
        'email': 'Test Email',
        'address': 'Test Address',
        'country': 'Test Country',
        'dept': 'Test Dept',
        'city': 'Test City',
        'phone': 1234567,
        'contact_name': 'Test Contact Name',
        'contact_phone': 1234567
      }

      company = CreateCompany(data, uuid4(), 2).execute()

      try:
        company = CreateCompany(data, uuid4(), 2).execute()
      except Exception as err:
        assert err.code == 409
        assert err.description == 'Company already exists'