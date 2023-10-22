from httmock import HTTMock, response, urlmatch

@urlmatch(path="/users/me")
def mock_success_auth(url, request):
  print(str(url.path))
  return response(200, { 'id': 1 }, {}, None, 5, request)

@urlmatch(path="/users/me")
def mock_failed_auth(url, request):
  print(url)
  return { 'status_code': 401 }

@urlmatch(path=r"/companies/.+")
def mock_company_found(url, request):
  print(str(url.path))
  return response(200, { 'id': 1 }, {}, None, 5, request)

@urlmatch(path=r"/update/companyID.+")
def mock_update_companyid(url, request):
  print(str(url.path))
  return response(200, { 'id': 1 }, {}, None, 5, request)