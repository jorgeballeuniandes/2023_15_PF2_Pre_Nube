from httmock import HTTMock, all_requests, response, urlmatch

@urlmatch(path="/users/me")
def mock_success_auth(url, request):
  print(str(url.path))
  return response(200, { 'id': 1 }, {}, None, 5, request)

@urlmatch(path=r"/it_specialists/.+")
def mock_it_specialist_found(url, request):
  print(str(url.path))
  return response(200, { 'id': 1 }, {}, None, 5, request)

@urlmatch(path=r"/it_specialists/.+")
def mock_it_specialist_not_found(url, request):
  print(str(url.path))
  return response(404, { 'id': 1 }, {}, "NOT FOUND", 5, request)

@urlmatch(path=r"/companies/.+")
def mock_company_found(url, request):
  return response(200, { 'id': 1 }, {}, None, 5, request)

@urlmatch(path=r"/companies/.+")
def mock_company_not_found(url, request):
  print(str(url.path))
  return response(404, { 'id': 1 }, {}, "NOT FOUND", 5, request)

@urlmatch(path=r"/projects/.+")
def mock_project_found(url, request):
  return response(200, { 'id': 1 }, {}, None, 5, request)

@urlmatch(path=r"/projects/.+")
def mock_project_not_found(url, request):
  print(str(url.path))
  return response(404, { 'id': 1 }, {}, "NOT FOUND", 5, request)

@urlmatch(path="/users/me")
def mock_failed_auth(url, request):
  print(url)
  return { 'status_code': 401 }