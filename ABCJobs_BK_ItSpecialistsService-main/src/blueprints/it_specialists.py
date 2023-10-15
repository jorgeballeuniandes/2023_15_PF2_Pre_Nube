from flask import Flask, jsonify, request, Blueprint
from ..commands.create_it_specialist import CreateItSpecialist
from ..commands.get_it_specialist import GetItSpecialist
from ..commands.get_it_specialists import GetItSpecialists
from ..commands.get_it_specialist_by_user_id import GetItSpecialistByUserId
from ..commands.public_create_it_specialist import PublicCreateItSpecialist
from ..commands.authenticate import Authenticate
from ..commands.reset import Reset

it_specialists_blueprint = Blueprint('it_specialists', __name__)

@it_specialists_blueprint.route('/it_specialists', methods = ['POST'])
def create():
    auth_info = Authenticate(auth_token()).execute()
    it_specialist = CreateItSpecialist(request.get_json(), auth_info['id']).execute()
    return jsonify(it_specialist), 201

@it_specialists_blueprint.route('/public/it_specialists', methods = ['POST'])
def public_create():
    auth_info = Authenticate(auth_token()).execute()
    it_specialist = PublicCreateItSpecialist(request.get_json(), auth_info['id']).execute()
    return jsonify(it_specialist), 201

@it_specialists_blueprint.route('/it_specialists', methods = ['GET'])
def index():
    auth_info = Authenticate(auth_token()).execute()
    it_specialists = GetItSpecialists(request.args.to_dict(), auth_info['id']).execute()
    return jsonify(it_specialists)

@it_specialists_blueprint.route('/it_specialists/<id>', methods = ['GET'])
def show(id):
    Authenticate(auth_token()).execute()
    it_specialist = GetItSpecialist(id).execute()
    return jsonify(it_specialist)

@it_specialists_blueprint.route('/it_specialists/ping', methods = ['GET'])
def ping():
    return 'pong'

@it_specialists_blueprint.route('/it_specialists/reset', methods = ['POST'])
def reset():
    Reset().execute()
    return jsonify({'status': 'OK'})

def auth_token():
    if 'Authorization' in request.headers:
        authorization = request.headers['Authorization']
    else:
        authorization = None
    return authorization