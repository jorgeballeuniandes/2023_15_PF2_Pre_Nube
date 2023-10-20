from flask import Flask, jsonify, request, Blueprint
from ..commands.create_interview import CreateInterview
from ..commands.get_interview import GetInterview
from ..commands.get_interviews import GetInterviews
from ..commands.authenticate import Authenticate
from ..commands.reset import Reset

interviews_blueprint = Blueprint('interviews', __name__)

@interviews_blueprint.route('/interviews', methods = ['POST'])
def create():
    auth_info = Authenticate(auth_token()).execute()
    interview = CreateInterview(request.get_json(), auth_token()).execute()
    return jsonify(interview), 201
@interviews_blueprint.route('/interviews', methods = ['GET'])
def index():
    auth_info = Authenticate(auth_token()).execute()
    interviews = GetInterviews().execute()
    return jsonify(interviews)

@interviews_blueprint.route('/interviews/<id>', methods = ['GET'])
def show(id):
    Authenticate(auth_token()).execute()
    interview = GetInterview(id).execute()
    return jsonify(interview)

@interviews_blueprint.route('/', methods = ['GET'])
def ping():
    return 'pong'

@interviews_blueprint.route('/interviews/reset', methods = ['POST'])
def reset():
    Reset().execute()
    return jsonify({'status': 'OK'})


def auth_token():
    if 'Authorization' in request.headers:
        authorization = request.headers['Authorization']
    else:
        authorization = None
    return authorization