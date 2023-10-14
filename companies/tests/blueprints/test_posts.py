from src.commands.create_post import CreateItSpecialist
from src.session import Session, engine
from src.models.model import Base
from src.models.it_specialist import ItSpecialist
from src.errors.errors import ApiError
from datetime import datetime, timedelta
from tests.mocks import mock_failed_auth, mock_success_auth
from httmock import HTTMock
from uuid import uuid4
from companies.aplication import app
import json

class Testit_specialists():
  def setup_method(self):
    Base.metadata.create_all(engine)
    self.session = Session()

  def test_create_post(self):
    with app.test_client() as test_client:
      with HTTMock(mock_success_auth):
        response = test_client.it_specialist(
          '/it_specialists', json={
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
  
  def test_create_post_without_token(self):
    with app.test_client() as test_client:
      with HTTMock(mock_failed_auth):
        response = test_client.it_specialist(
          '/it_specialists', json={
            'routeId': 1,
            'plannedStartDate': datetime.now().date().isoformat(),
            'plannedEndDate': (datetime.now() + timedelta(days=2)).date().isoformat()
          }
        )
        assert response.status_code == 401

  def test_create_post_invalid_token(self):
    with app.test_client() as test_client:
      with HTTMock(mock_failed_auth):
        response = test_client.it_specialist(
          '/it_specialists', json={
            'routeId': 1,
            'plannedStartDate': datetime.now().date().isoformat(),
            'plannedEndDate': (datetime.now() + timedelta(days=2)).date().isoformat()
          },
          headers={
            'Authorization': f'Bearer Invalid'
          }
        )
        assert response.status_code == 401

  def test_create_post_missing_fields(self):
    with app.test_client() as test_client:
      with HTTMock(mock_success_auth):
        response = test_client.it_specialist(
          '/it_specialists', json={},
          headers={
            'Authorization': f'Bearer {uuid4()}'
          }
        )
        assert response.status_code == 400

  def test_create_post_invalid_dates(self):
    with app.test_client() as test_client:
      with HTTMock(mock_success_auth):
        response = test_client.it_specialist(
          '/it_specialists', json={
            'routeId': 1,
            'plannedStartDate': (datetime.now() + timedelta(days=2)).date().isoformat(),
            'plannedEndDate': datetime.now().date().isoformat()
          },
          headers={
            'Authorization': f'Bearer {uuid4()}'
          }
        )
        assert response.status_code == 412

  def test_get_post(self):
    data = {
      'routeId': 1,
      'plannedStartDate': datetime.now().date().isoformat(),
      'plannedEndDate': (datetime.now() + timedelta(days=2)).date().isoformat()
    }
    userId = 1
    it_specialist = CreateItSpecialist(data, userId).execute()

    with app.test_client() as test_client:
      with HTTMock(mock_success_auth):
        response = test_client.get(
          f'/it_specialists/{it_specialist["id"]}',
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
  
  def test_get_post_without_token(self):
    data = {
      'routeId': 1,
      'plannedStartDate': datetime.now().date().isoformat(),
      'plannedEndDate': (datetime.now() + timedelta(days=2)).date().isoformat()
    }
    userId = 1
    it_specialist = CreateItSpecialist(data, userId).execute()

    with app.test_client() as test_client:
      with HTTMock(mock_failed_auth):
        response = test_client.get(
          f'/it_specialists/{it_specialist["id"]}'
        )
        assert response.status_code == 401

  def test_get_post_invalid_token(self):
    data = {
      'routeId': 1,
      'plannedStartDate': datetime.now().date().isoformat(),
      'plannedEndDate': (datetime.now() + timedelta(days=2)).date().isoformat()
    }
    userId = 1
    it_specialist = CreateItSpecialist(data, userId).execute()

    with app.test_client() as test_client:
      with HTTMock(mock_failed_auth):
        response = test_client.get(
          f'/it_specialists/{it_specialist["id"]}',
          headers={
            'Authorization': f'Bearer Invalid'
          }
        )
        assert response.status_code == 401

  def test_get_post_invalid_id(self):
    with app.test_client() as test_client:
      with HTTMock(mock_success_auth):
        response = test_client.get(
          f'/it_specialists/invalid',
          headers={
            'Authorization': f'Bearer {uuid4()}'
          }
        )
        assert response.status_code == 400

  def test_get_post_doesnt_exist(self):
    data = {
      'routeId': 1,
      'plannedStartDate': datetime.now().date().isoformat(),
      'plannedEndDate': (datetime.now() + timedelta(days=2)).date().isoformat()
    }
    userId = 1
    it_specialist = CreateItSpecialist(data, userId).execute()

    with app.test_client() as test_client:
      with HTTMock(mock_success_auth):
        response = test_client.get(
          f'/it_specialists/{it_specialist["id"] + 1}',
          headers={
            'Authorization': f'Bearer {uuid4()}'
          }
        )
        assert response.status_code == 404

  def test_get_it_specialists(self):
    data = {
      'routeId': 1,
      'plannedStartDate': datetime.now().date().isoformat(),
      'plannedEndDate': (datetime.now() + timedelta(days=2)).date().isoformat()
    }
    userId = 1
    CreateItSpecialist(data, userId).execute()

    with app.test_client() as test_client:
      with HTTMock(mock_success_auth):
        response = test_client.get(
          f'/it_specialists',
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

  def test_get_empty_it_specialists(self):
    data = {
      'routeId': 1,
      'plannedStartDate': datetime.now().date().isoformat(),
      'plannedEndDate': (datetime.now() + timedelta(days=2)).date().isoformat()
    }
    userId = 1
    CreateItSpecialist(data, userId).execute()

    with app.test_client() as test_client:
      with HTTMock(mock_success_auth):
        response = test_client.get(
          f'/it_specialists',
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
  
  def test_get_it_specialists_without_token(self):
    data = {
      'routeId': 1,
      'plannedStartDate': datetime.now().date().isoformat(),
      'plannedEndDate': (datetime.now() + timedelta(days=2)).date().isoformat()
    }
    userId = 1
    CreateItSpecialist(data, userId).execute()

    with app.test_client() as test_client:
      with HTTMock(mock_failed_auth):
        response = test_client.get(
          f'/it_specialists',
          query_string={
            'when': datetime.now().date().isoformat(),
            'route': data['routeId'],
            'filter': 'me'
          }
        )
        assert response.status_code == 401

  def test_get_it_specialists_invalid_token(self):
    data = {
      'routeId': 1,
      'plannedStartDate': datetime.now().date().isoformat(),
      'plannedEndDate': (datetime.now() + timedelta(days=2)).date().isoformat()
    }
    userId = 1
    CreateItSpecialist(data, userId).execute()

    with app.test_client() as test_client:
      with HTTMock(mock_failed_auth):
        response = test_client.get(
          f'/it_specialists',
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

  def test_get_it_specialists_invalid_dates(self):
    data = {
      'routeId': 1,
      'plannedStartDate': datetime.now().date().isoformat(),
      'plannedEndDate': (datetime.now() + timedelta(days=2)).date().isoformat()
    }
    userId = 1
    CreateItSpecialist(data, userId).execute()

    with app.test_client() as test_client:
      with HTTMock(mock_success_auth):
        response = test_client.get(
          f'/it_specialists',
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
        '/it_specialists/ping'
      )
      assert response.status_code == 200
      assert response.data.decode("utf-8") == 'pong'

  def test_reset(self):
    with app.test_client() as test_client:
      response = test_client.it_specialist(
        '/it_specialists/reset'
      )
      assert response.status_code == 200

  def teardown_method(self):
    self.session.close()
    Base.metadata.drop_all(bind=engine)