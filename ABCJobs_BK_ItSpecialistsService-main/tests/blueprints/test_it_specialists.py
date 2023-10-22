from src.commands.create_it_specialist import CreateItSpecialist
from src.session import Session, engine
from src.models.model import Base
from src.models.it_specialist import ItSpecialist
from src.errors.errors import ApiError
from datetime import datetime, timedelta
from tests.mocks import mock_failed_auth, mock_success_auth
from httmock import HTTMock
from uuid import uuid4
from application import application
import json

class TestItSpecialists():
  def setup_method(self):
    Base.metadata.create_all(engine)
    self.session = Session()

  def test_create_it_specialist(self):
    with application.test_client() as test_client:
      with HTTMock(mock_success_auth):
        response = test_client.post(
          '/it_specialists', json={
              "userId":1,
              "name":"juan",
              "email":"juan@gmail.com",
              "nationality":"Colombia",
              "profession":"Developer",
              "speciality":".NET Junior Developer",
              "profile":"Great developer"
          },
          headers={
            'Authorization': f'Bearer {uuid4()}'
          }
        )
        response_json = json.loads(response.data)
        assert response.status_code == 201
        assert 'id' in response_json
        assert 'userId' in response_json
        assert 'name' in response_json
        assert 'email' in response_json
        assert 'nationality' in response_json
        assert 'profession' in response_json
        assert 'speciality' in response_json
        assert 'profile' in response_json
  
  def test_create_it_specialist_without_token(self):
    with application.test_client() as test_client:
      with HTTMock(mock_failed_auth):
        response = test_client.post(
          '/it_specialists', json={
              "userId":1,
              "name":"juan",
              "email":"juan@gmail.com",
              "nationality":"Colombia",
              "profession":"Developer",
              "speciality":".NET Junior Developer",
              "profile":"Great developer"
          }
        )
        assert response.status_code == 401

  def test_create_it_specialist_invalid_token(self):
    with application.test_client() as test_client:
      with HTTMock(mock_failed_auth):
        response = test_client.post(
          '/it_specialists', json={
              "userId":1,
              "name":"juan",
              "email":"juan@gmail.com",
              "nationality":"Colombia",
              "profession":"Developer",
              "speciality":".NET Junior Developer",
              "profile":"Great developer"
          },
          headers={
            'Authorization': f'Bearer Invalid'
          }
        )
        assert response.status_code == 401

  def test_create_it_specialist_missing_fields(self):
    with application.test_client() as test_client:
      with HTTMock(mock_success_auth):
        response = test_client.post(
          '/it_specialists', json={},
          headers={
            'Authorization': f'Bearer {uuid4()}'
          }
        )
        assert response.status_code == 400

  def test_get_it_specialist(self):
    data = {  
              "userId":1,
              "name":"juan",
              "email":"juan@gmail.com",
              "nationality":"Colombia",
              "profession":"Developer",
              "speciality":".NET Junior Developer",
              "profile":"Great developer"
    }
    userId = 1
    it_specialist = CreateItSpecialist(data, userId).execute()

    with application.test_client() as test_client:
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
        assert 'userId' in response_json
        assert 'name' in response_json
        assert 'email' in response_json
        assert 'nationality' in response_json
        assert 'profession' in response_json
        assert 'speciality' in response_json
        assert 'profile' in response_json
  
  def test_get_it_specialist_without_token(self):
    data = {
              "userId":1,
              "name":"juan",
              "email":"juan@gmail.com",
              "nationality":"Colombia",
              "profession":"Developer",
              "speciality":".NET Junior Developer",
              "profile":"Great developer"
    }
    userId = 1
    it_specialist = CreateItSpecialist(data, userId).execute()

    with application.test_client() as test_client:
      with HTTMock(mock_failed_auth):
        response = test_client.get(
          f'/it_specialists/{it_specialist["id"]}'
        )
        assert response.status_code == 401

  def test_get_it_specialist_invalid_token(self):
    data = {
              "userId":1,
              "name":"juan",
              "email":"juan@gmail.com",
              "nationality":"Colombia",
              "profession":"Developer",
              "speciality":".NET Junior Developer",
              "profile":"Great developer"
    }
    userId = 1
    it_specialist = CreateItSpecialist(data, userId).execute()

    with application.test_client() as test_client:
      with HTTMock(mock_failed_auth):
        response = test_client.get(
          f'/it_specialists/{it_specialist["id"]}',
          headers={
            'Authorization': f'Bearer Invalid'
          }
        )
        assert response.status_code == 401

  def test_get_it_specialist_invalid_id(self):
    with application.test_client() as test_client:
      with HTTMock(mock_success_auth):
        response = test_client.get(
          f'/it_specialists/invalid',
          headers={
            'Authorization': f'Bearer {uuid4()}'
          }
        )
        assert response.status_code == 400

  def test_get_it_specialist_doesnt_exist(self):
    data = {
              "userId":1,
              "name":"juan",
              "email":"juan@gmail.com",
              "nationality":"Colombia",
              "profession":"Developer",
              "speciality":".NET Junior Developer",
              "profile":"Great developer"
    }
    userId = 1
    it_specialist = CreateItSpecialist(data, userId).execute()

    with application.test_client() as test_client:
      with HTTMock(mock_success_auth):
        response = test_client.get(
          f'/it_specialists/{it_specialist["id"] + 1}',
          headers={
            'Authorization': f'Bearer {uuid4()}'
          }
        )
        assert response.status_code == 404

 
  def test_get_it_specialists_without_token(self):
    data = {
              "userId":1,
              "name":"juan",
              "email":"juan@gmail.com",
              "nationality":"Colombia",
              "profession":"Developer",
              "speciality":".NET Junior Developer",
              "profile":"Great developer"
    }
    userId = 1
    CreateItSpecialist(data, userId).execute()

    with application.test_client() as test_client:
      with HTTMock(mock_failed_auth):
        response = test_client.get(
          f'/it_specialists'
        )
        assert response.status_code == 401

  def test_get_it_specialists_invalid_token(self):
    data = {
              "userId":1,
              "name":"juan",
              "email":"juan@gmail.com",
              "nationality":"Colombia",
              "profession":"Developer",
              "speciality":".NET Junior Developer",
              "profile":"Great developer"
    }
    userId = 1
    CreateItSpecialist(data, userId).execute()

    with application.test_client() as test_client:
      with HTTMock(mock_failed_auth):
        response = test_client.get(
          f'/it_specialists',
          headers={
            'Authorization': f'Bearer Invalid'
          }
        )
        assert response.status_code == 401

  

  def test_ping(self):
    with application.test_client() as test_client:
      response = test_client.get(
        '/it_specialists/ping'
      )
      assert response.status_code == 200
      assert response.data.decode("utf-8") == 'pong'

  def test_reset(self):
    with application.test_client() as test_client:
      response = test_client.post(
        '/it_specialists/reset'
      )
      assert response.status_code == 200

  def teardown_method(self):
    self.session.close()
    Base.metadata.drop_all(bind=engine)