from src.commands.create_interview import CreateInterview
from src.session import Session, engine
from src.models.model import Base
from src.models.interview import Interview
from src.errors.errors import ApiError
from datetime import datetime, timedelta
from tests.mocks import mock_failed_auth, mock_success_auth, mock_it_specialist_found, mock_it_specialist_not_found, mock_company_found, mock_company_not_found, mock_project_found, mock_project_not_found
from httmock import HTTMock
from uuid import uuid4
from application import application
import json

class TestInterviews():
  def setup_method(self):
    Base.metadata.create_all(engine)
    self.session = Session()

  def test_create_post(self):
    with application.test_client() as test_client:
      with HTTMock(mock_success_auth,mock_project_found,mock_it_specialist_found, mock_company_found):
        response = test_client.post(
          '/interviews', json={
            "itSpecialistId": 1.0,
            "companyId": 1.0,
            "projectId": 1.0,
            "date": (datetime.now() + timedelta(days=2)).isoformat()
          },
          headers={
            'Authorization': f'Bearer {uuid4()}'
          }
        )
        response_json = json.loads(response.data)
        assert response.status_code == 201
        assert 'id' in response_json
        assert 'itSpecialistId' in response_json
        assert 'companyId' in response_json
        assert 'projectId' in response_json
        assert 'date' in response_json
  
  def test_create_post_without_token(self):
    with application.test_client() as test_client:
      with HTTMock(mock_failed_auth):
        response = test_client.post(
          '/interviews', json={
            "itSpecialistId": 1.0,
            "companyId": 1.0,
            "projectId": 1.0,
            "date": (datetime.now() + timedelta(days=2)).isoformat()
          }
        )
        assert response.status_code == 401

  def test_create_post_invalid_token(self):
    with application.test_client() as test_client:
      with HTTMock(mock_failed_auth):
        response = test_client.post(
          '/interviews', json={
            "itSpecialistId": 1.0,
            "companyId": 1.0,
            "projectId": 1.0,
            "date": (datetime.now() + timedelta(days=2)).isoformat()
          },
          headers={
            'Authorization': f'Bearer Invalid'
          }
        )
        assert response.status_code == 401

  def test_create_post_missing_fields(self):
    with application.test_client() as test_client:
      with HTTMock(mock_success_auth):
        response = test_client.post(
          '/interviews', json={},
          headers={
            'Authorization': f'Bearer {uuid4()}'
          }
        )
        assert response.status_code == 400

  def test_create_post_invalid_it_specialist(self):
    with application.test_client() as test_client:
      with HTTMock(mock_success_auth, mock_it_specialist_not_found):
        response = test_client.post(
          '/interviews', json={
            "itSpecialistId": 1.0,
            "companyId": 1.0,
            "projectId": 1.0,
            "date": (datetime.now() + timedelta(days=2)).isoformat()
          },
          headers={
            'Authorization': f'Bearer {uuid4()}'
          }
        )
        response_json = json.loads(response.data)
        assert response.status_code == 404
        assert 'mssg' in response_json
        assert 'It Specialist Error: ' in response_json['mssg']

  def test_create_post_invalid_company(self):
    with application.test_client() as test_client:
      with HTTMock(mock_success_auth, mock_it_specialist_found, mock_company_not_found):
        response = test_client.post(
          '/interviews', json={
            "itSpecialistId": 1.0,
            "companyId": 1.0,
            "projectId": 1.0,
            "date": (datetime.now() + timedelta(days=2)).isoformat()
          },
          headers={
            'Authorization': f'Bearer {uuid4()}'
          }
        )
        response_json = json.loads(response.data)
        assert response.status_code == 404
        assert 'mssg' in response_json
        assert 'Company Error: ' in response_json['mssg']

  def test_create_post_invalid_project(self):
    with application.test_client() as test_client:
      with HTTMock(mock_success_auth, mock_it_specialist_found, mock_company_found, mock_project_not_found):
        response = test_client.post(
          '/interviews', json={
            "itSpecialistId": 1.0,
            "companyId": 1.0,
            "projectId": 1.0,
            "date": (datetime.now() + timedelta(days=2)).isoformat()
          },
          headers={
            'Authorization': f'Bearer {uuid4()}'
          }
        )
        response_json = json.loads(response.data)
        assert response.status_code == 404
        assert 'mssg' in response_json
        assert 'Project Error: ' in response_json['mssg']

  def test_get_interview(self):
    data = {
      "itSpecialistId": 1.0,
      "companyId": 1.0,
      "projectId": 1.0,
      "date": (datetime.now() + timedelta(days=2)).isoformat()
    }
    userId = 1

    with application.test_client() as test_client:
      with HTTMock(mock_success_auth, mock_it_specialist_found, mock_company_found, mock_project_found):
        interview = CreateInterview(data, userId).execute()
        response = test_client.get(
          f'/interviews/{interview["id"]}',
          headers={
            'Authorization': f'Bearer {uuid4()}'
          }
        )
        response_json = json.loads(response.data)
        assert response.status_code == 200
        assert 'id' in response_json
        assert 'itSpecialistId' in response_json
        assert 'companyId' in response_json
        assert 'projectId' in response_json
        assert 'date' in response_json
  
  def test_get_interview_without_token(self):

    with application.test_client() as test_client:
      with HTTMock(mock_failed_auth):
        response = test_client.get(
          f'/interviews/1'
        )
        assert response.status_code == 401

  def test_get_interview_invalid_token(self):

    with application.test_client() as test_client:
      with HTTMock(mock_failed_auth):
        response = test_client.get(
          f'/interviews/1',
          headers={
            'Authorization': f'Bearer Invalid'
          }
        )
        assert response.status_code == 401

  def test_get_interview_invalid_id(self):
    with application.test_client() as test_client:
      with HTTMock(mock_success_auth):
        response = test_client.get(
          f'/interviews/invalid',
          headers={
            'Authorization': f'Bearer {uuid4()}'
          }
        )
        assert response.status_code == 400

  def test_get_interview_doesnt_exist(self):
    data = {
      "itSpecialistId": 1.0,
      "companyId": 1.0,
      "projectId": 1.0,
      "date": (datetime.now() + timedelta(days=2)).isoformat()
    }
    userId = 1

    with application.test_client() as test_client:
      with HTTMock(mock_success_auth, mock_it_specialist_found, mock_company_found, mock_project_found):
        interview = CreateInterview(data, userId).execute()
        response = test_client.get(
          f'/interviews/{interview["id"] + 1}',
          headers={
            'Authorization': f'Bearer {uuid4()}'
          }
        )
        assert response.status_code == 404

  def test_get_interviews(self):
    data = {
      "itSpecialistId": 1.0,
      "companyId": 1.0,
      "projectId": 1.0,
      "date": (datetime.now() + timedelta(days=2)).isoformat()
    }
    userId = 1

    with application.test_client() as test_client:
      with HTTMock(mock_success_auth, mock_it_specialist_found, mock_company_found, mock_project_found):
        CreateInterview(data, userId).execute()
        response = test_client.get(
          f'/interviews',
          headers={
            'Authorization': f'Bearer {uuid4()}'
          }
        )
        response_json = json.loads(response.data)
        assert response.status_code == 200
        assert len(response_json) == 1
        assert 'id' in response_json[0]
        assert 'itSpecialistId' in response_json[0]
        assert 'companyId' in response_json[0]
        assert 'projectId' in response_json[0]
        assert 'date' in response_json[0]

  def test_ping(self):
    with application.test_client() as test_client:
      response = test_client.get(
        '/'
      )
      assert response.status_code == 200
      assert response.data.decode("utf-8") == 'pong'

  def test_reset(self):
    with application.test_client() as test_client:
      response = test_client.post(
        '/interviews/reset'
      )
      assert response.status_code == 200

  def teardown_method(self):
    self.session.close()
    Base.metadata.drop_all(bind=engine)