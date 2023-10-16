from src.commands.create_it_specialist_document import CreateItSpecialistDocument
from src.session import Session, engine
from src.models.model import Base
from src.models.it_specialist_document import ItSpecialistDocument
from src.errors.errors import ApiError
from datetime import datetime, timedelta
from tests.mocks import mock_failed_auth, mock_success_auth
from httmock import HTTMock
from uuid import uuid4
from application import app
import json

class Testit_specialist_documents():
  def setup_method(self):
    Base.metadata.create_all(engine)
    self.session = Session()

  def test_create_it_specialist_document(self):
    with app.test_client() as test_client:
      with HTTMock(mock_success_auth):
        response = test_client.it_specialist_document(
          '/it_specialist_documents', json={
            'routeId': 1,
            'plannedStartDate': datetime.now().date().isoformat(),
            'plannedEndDate': (datetime.now() + timedelta(days=2)).date().isoformat()
          },
          headers={
            'Authorization': f'Bearer {uuid4()}'
          }
        )
        response_json = json.loads(response.data)
        assert response.status_code == 201
        assert 'id' in response_json
        assert 'userId' in response_json
        assert 'createdAt' in response_json
  
  def test_create_it_specialist_document_without_token(self):
    with app.test_client() as test_client:
      with HTTMock(mock_failed_auth):
        response = test_client.it_specialist_document(
          '/it_specialist_documents', json={
            'routeId': 1,
            'plannedStartDate': datetime.now().date().isoformat(),
            'plannedEndDate': (datetime.now() + timedelta(days=2)).date().isoformat()
          }
        )
        assert response.status_code == 401

  def test_create_it_specialist_document_invalid_token(self):
    with app.test_client() as test_client:
      with HTTMock(mock_failed_auth):
        response = test_client.it_specialist_document(
          '/it_specialist_documents', json={
            'routeId': 1,
            'plannedStartDate': datetime.now().date().isoformat(),
            'plannedEndDate': (datetime.now() + timedelta(days=2)).date().isoformat()
          },
          headers={
            'Authorization': f'Bearer Invalid'
          }
        )
        assert response.status_code == 401

  def test_create_it_specialist_document_missing_fields(self):
    with app.test_client() as test_client:
      with HTTMock(mock_success_auth):
        response = test_client.it_specialist_document(
          '/it_specialist_documents', json={},
          headers={
            'Authorization': f'Bearer {uuid4()}'
          }
        )
        assert response.status_code == 400

  def test_create_it_specialist_document_invalid_dates(self):
    with app.test_client() as test_client:
      with HTTMock(mock_success_auth):
        response = test_client.it_specialist_document(
          '/it_specialist_documents', json={
            'routeId': 1,
            'plannedStartDate': (datetime.now() + timedelta(days=2)).date().isoformat(),
            'plannedEndDate': datetime.now().date().isoformat()
          },
          headers={
            'Authorization': f'Bearer {uuid4()}'
          }
        )
        assert response.status_code == 412

  def test_get_it_specialist_document(self):
    data = {
      'routeId': 1,
      'plannedStartDate': datetime.now().date().isoformat(),
      'plannedEndDate': (datetime.now() + timedelta(days=2)).date().isoformat()
    }
    userId = 1
    it_specialist_document = CreateItSpecialistDocument(data, userId).execute()

    with app.test_client() as test_client:
      with HTTMock(mock_success_auth):
        response = test_client.get(
          f'/it_specialist_documents/{it_specialist_document["id"]}',
          headers={
            'Authorization': f'Bearer {uuid4()}'
          }
        )
        response_json = json.loads(response.data)
        assert response.status_code == 200
        assert 'id' in response_json
        assert 'routeId' in response_json
        assert 'userId' in response_json
        assert 'plannedStartDate' in response_json
        assert 'plannedEndDate' in response_json
        assert 'createdAt' in response_json
  
  def test_get_it_specialist_document_without_token(self):
    data = {
      'routeId': 1,
      'plannedStartDate': datetime.now().date().isoformat(),
      'plannedEndDate': (datetime.now() + timedelta(days=2)).date().isoformat()
    }
    userId = 1
    it_specialist_document = CreateItSpecialistDocument(data, userId).execute()

    with app.test_client() as test_client:
      with HTTMock(mock_failed_auth):
        response = test_client.get(
          f'/it_specialist_documents/{it_specialist_document["id"]}'
        )
        assert response.status_code == 401

  def test_get_it_specialist_document_invalid_token(self):
    data = {
      'routeId': 1,
      'plannedStartDate': datetime.now().date().isoformat(),
      'plannedEndDate': (datetime.now() + timedelta(days=2)).date().isoformat()
    }
    userId = 1
    it_specialist_document = CreateItSpecialistDocument(data, userId).execute()

    with app.test_client() as test_client:
      with HTTMock(mock_failed_auth):
        response = test_client.get(
          f'/it_specialist_documents/{it_specialist_document["id"]}',
          headers={
            'Authorization': f'Bearer Invalid'
          }
        )
        assert response.status_code == 401

  def test_get_it_specialist_document_invalid_id(self):
    with app.test_client() as test_client:
      with HTTMock(mock_success_auth):
        response = test_client.get(
          f'/it_specialist_documents/invalid',
          headers={
            'Authorization': f'Bearer {uuid4()}'
          }
        )
        assert response.status_code == 400

  def test_get_it_specialist_document_doesnt_exist(self):
    data = {
      'routeId': 1,
      'plannedStartDate': datetime.now().date().isoformat(),
      'plannedEndDate': (datetime.now() + timedelta(days=2)).date().isoformat()
    }
    userId = 1
    it_specialist_document = CreateItSpecialistDocument(data, userId).execute()

    with app.test_client() as test_client:
      with HTTMock(mock_success_auth):
        response = test_client.get(
          f'/it_specialist_documents/{it_specialist_document["id"] + 1}',
          headers={
            'Authorization': f'Bearer {uuid4()}'
          }
        )
        assert response.status_code == 404

  def test_get_it_specialist_documents(self):
    data = {
      'routeId': 1,
      'plannedStartDate': datetime.now().date().isoformat(),
      'plannedEndDate': (datetime.now() + timedelta(days=2)).date().isoformat()
    }
    userId = 1
    CreateItSpecialistDocument(data, userId).execute()

    with app.test_client() as test_client:
      with HTTMock(mock_success_auth):
        response = test_client.get(
          f'/it_specialist_documents',
          query_string={
            'when': datetime.now().date().isoformat(),
            'route': data['routeId'],
            'filter': 'me'
          },
          headers={
            'Authorization': f'Bearer {uuid4()}'
          }
        )
        response_json = json.loads(response.data)
        assert response.status_code == 200
        assert len(response_json) == 1
        assert 'id' in response_json[0]
        assert 'routeId' in response_json[0]
        assert 'userId' in response_json[0]
        assert 'plannedStartDate' in response_json[0]
        assert 'plannedEndDate' in response_json[0]
        assert 'createdAt' in response_json[0]

  def test_get_empty_it_specialist_documents(self):
    data = {
      'routeId': 1,
      'plannedStartDate': datetime.now().date().isoformat(),
      'plannedEndDate': (datetime.now() + timedelta(days=2)).date().isoformat()
    }
    userId = 1
    CreateItSpecialistDocument(data, userId).execute()

    with app.test_client() as test_client:
      with HTTMock(mock_success_auth):
        response = test_client.get(
          f'/it_specialist_documents',
          query_string={
            'when': (datetime.now() + timedelta(days=3)).date().isoformat(),
            'route': data['routeId'],
            'filter': 'me'
          },
          headers={
            'Authorization': f'Bearer {uuid4()}'
          }
        )
        response_json = json.loads(response.data)
        assert response.status_code == 200
        assert len(response_json) == 0
  
  def test_get_it_specialist_documents_without_token(self):
    data = {
      'routeId': 1,
      'plannedStartDate': datetime.now().date().isoformat(),
      'plannedEndDate': (datetime.now() + timedelta(days=2)).date().isoformat()
    }
    userId = 1
    CreateItSpecialistDocument(data, userId).execute()

    with app.test_client() as test_client:
      with HTTMock(mock_failed_auth):
        response = test_client.get(
          f'/it_specialist_documents',
          query_string={
            'when': datetime.now().date().isoformat(),
            'route': data['routeId'],
            'filter': 'me'
          }
        )
        assert response.status_code == 401

  def test_get_it_specialist_documents_invalid_token(self):
    data = {
      'routeId': 1,
      'plannedStartDate': datetime.now().date().isoformat(),
      'plannedEndDate': (datetime.now() + timedelta(days=2)).date().isoformat()
    }
    userId = 1
    CreateItSpecialistDocument(data, userId).execute()

    with app.test_client() as test_client:
      with HTTMock(mock_failed_auth):
        response = test_client.get(
          f'/it_specialist_documents',
          query_string={
            'when': datetime.now().date().isoformat(),
            'route': data['routeId'],
            'filter': 'me'
          },
          headers={
            'Authorization': f'Bearer Invalid'
          }
        )
        assert response.status_code == 401

  def test_get_it_specialist_documents_invalid_dates(self):
    data = {
      'routeId': 1,
      'plannedStartDate': datetime.now().date().isoformat(),
      'plannedEndDate': (datetime.now() + timedelta(days=2)).date().isoformat()
    }
    userId = 1
    CreateItSpecialistDocument(data, userId).execute()

    with app.test_client() as test_client:
      with HTTMock(mock_success_auth):
        response = test_client.get(
          f'/it_specialist_documents',
          query_string={
            'when': 'invalid',
            'route': data['routeId'],
            'filter': 'me'
          },
          headers={
            'Authorization': f'Bearer {uuid4()}'
          }
        )
        assert response.status_code == 400

  def test_ping(self):
    with app.test_client() as test_client:
      response = test_client.get(
        '/it_specialist_documents/ping'
      )
      assert response.status_code == 200
      assert response.data.decode("utf-8") == 'pong'

  def test_reset(self):
    with app.test_client() as test_client:
      response = test_client.it_specialist_document(
        '/it_specialist_documents/reset'
      )
      assert response.status_code == 200

  def teardown_method(self):
    self.session.close()
    Base.metadata.drop_all(bind=engine)