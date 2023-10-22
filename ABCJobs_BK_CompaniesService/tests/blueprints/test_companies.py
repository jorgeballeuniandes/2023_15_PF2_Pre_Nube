from src.session import Session, engine
from src.models.model import Base
from tests.mocks import mock_failed_auth, mock_success_auth, mock_company_found, mock_update_companyid
from httmock import HTTMock
from uuid import uuid4
import json
from application import application

from httmock import HTTMock, response, urlmatch
from faker import Faker

class TestCompaniesBlueprint():
    def setup_method(self):
      Base.metadata.create_all(engine)
      self.session = Session()

    def test_create_company(self):
      with application.test_client() as client:
          with HTTMock(mock_success_auth, mock_company_found, mock_update_companyid):
              fake = Faker()
              response = client.post(
                  '/companies', 
                  json={
                      'name': fake.name(),
                      'email': 'Test Email',
                      'address': 'Test Address',
                      'country': 'Test Country',
                      'dept': 'Test Dept',
                      'city': 'Test City',
                      'phone': 1234567,
                      'contact_name': 'Test Contact Name',
                      'contact_phone': 1234567
                  },
                  headers={
                     'Authorization': f'Bearer {uuid4()}'
                     }
              )
              response_json = json.loads(response.data)

              assert response.status_code == 201
              assert 'companyId' in response_json
              assert 'name' in response_json

    def test_create_company_with_invalid_token(self):
      with application.test_client() as client:
          with HTTMock(mock_failed_auth):
              fake = Faker()
              response = client.post(
                  '/companies', 
                  json={
                      'name': fake.name(),
                      'email': 'Test Email',
                      'address': 'Test Address',
                      'country': 'Test Country',
                      'dept': 'Test Dept',
                      'city': 'Test City',
                      'phone': 1234567,
                      'contact_name': 'Test Contact Name',
                      'contact_phone': 1234567
                  },
                  headers={
                     'Authorization': f'Bearer {uuid4()}'
                     }
              )
              response_json = json.loads(response.data)

              assert response.status_code == 401
              assert 'companyId' not in response_json
              assert 'name' not in response_json
  
    def test_create_company_with_invalid_params(self):
      with application.test_client() as client:
          with HTTMock(mock_success_auth):
              fake = Faker()
              response = client.post(
                  '/companies', 
                  json={
                      'name': fake.name(),
                      'email': 'Test Email',
                      'address': 'Test Address',
                      'country': 'Test Country',
                      'dept': 'Test Dept',
                      'city': 'Test City',
                      'phone': 1234567,
                      'contact_name': 'Test Contact Name',
                  },
                  headers={
                     'Authorization': f'Bearer {uuid4()}'
                     }
              )
              response_json = json.loads(response.data)

              assert response.status_code == 400
              assert 'companyId' not in response_json
              assert 'name' not in response_json

    def test_create_company_with_existing_name(self):
      with application.test_client() as client:
          with HTTMock(mock_success_auth, mock_company_found):
              client.post(
                  '/companies', 
                  json={
                      'name': 'Test Name',
                      'email': 'Test Email',
                      'address': 'Test Address',
                      'country': 'Test Country',
                      'dept': 'Test Dept',
                      'city': 'Test City',
                      'phone': 1234567,
                      'contact_name': 'Test Contact Name',
                      'contact_phone': 1234567
                  },
                  headers={
                     'Authorization': f'Bearer {uuid4()}'
                     }
              )
              response = client.post(
                  '/companies', 
                  json={
                      'name': 'Test Name',
                      'email': 'Test Email',
                      'address': 'Test Address',
                      'country': 'Test Country',
                      'dept': 'Test Dept',
                      'city': 'Test City',
                      'phone': 1234567,
                      'contact_name': 'Test Contact Name',
                      'contact_phone': 1234567
                  },
                  headers={
                     'Authorization': f'Bearer {uuid4()}'
                     }
              )

              response_json = json.loads(response.data)

              assert response.status_code == 409
              assert 'companyId' not in response_json
              assert 'name' not in response_json
   
    def test_get_company(self):
      with application.test_client() as client:
          with HTTMock(mock_success_auth):
              
              response = client.get('companies')
              response_json = json.loads(response.data)

              assert response.status_code == 200
              assert 'companyId' in response_json[0]
              assert 'name' in response_json[0]
    
    def test_get_companies(self):
      with application.test_client() as client:
          with HTTMock(mock_success_auth):
              
              client.post(
                  '/companies', 
                  json={
                      'name': 'Test Name',
                      'email': 'Test Email',
                      'address': 'Test Address',
                      'country': 'Test Country',
                      'dept': 'Test Dept',
                      'city': 'Test City',
                      'phone': 1234567,
                      'contact_name': 'Test Contact Name',
                      'contact_phone': 1234567
                  },
                  headers={
                     'Authorization': f'Bearer {uuid4()}'
                     }
              )

              response = client.get('companies/1')
              response_json = json.loads(response.data)

              assert response.status_code == 200
              assert 'companyId' in response_json
              assert 'name' in response_json
    

    def test_get_companies_invalid_id(self):
      with application.test_client() as client:
        with HTTMock(mock_success_auth):
          response = client.get('companies/invalid_id')
          response_json = json.loads(response.data)

          assert response.status_code == 400
          assert response_json['mssg'] == 'Bad request'

    def test_ping(self):
      with application.test_client() as client:
        # Make a GET request to /companies/ping
        response = client.get('/companies/ping')

        # Verify that the response is correct
        assert response.status_code == 200
        assert response.data.decode('utf-8'), 'pong'