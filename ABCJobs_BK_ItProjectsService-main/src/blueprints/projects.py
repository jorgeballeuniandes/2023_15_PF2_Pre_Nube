from flask import Flask, jsonify, request, Blueprint
from ..commands.create_project import CreateProject
from ..commands.get_project import GetProject
from ..commands.get_projects import GetProjects
from ..commands.authenticate import Authenticate
from ..commands.reset import Reset

projects_blueprint = Blueprint('projects', __name__)

@projects_blueprint.route('/projects', methods = ['POST'])
def create():
    auth_info = Authenticate(auth_token()).execute()
    project = CreateProject(request.get_json(), auth_info['id']).execute()
    return jsonify(project), 201

@projects_blueprint.route('/projects', methods = ['GET'])
def index():
    auth_info = Authenticate(auth_token()).execute()
    projects = GetProjects(request.args.to_dict(), auth_info['id']).execute()
    return jsonify(projects)

@projects_blueprint.route('/projects/<id>', methods = ['GET'])
def show(id):
    Authenticate(auth_token()).execute()
    project = GetProject(id).execute()
    return jsonify(project)

@projects_blueprint.route('/projects/ping', methods = ['GET'])
def ping():
    return 'pong'

@projects_blueprint.route('/projects/reset', methods = ['POST'])
def reset():
    Reset().execute()
    return jsonify({'status': 'OK'})

def auth_token():
    if 'Authorization' in request.headers:
        authorization = request.headers['Authorization']
    else:
        authorization = None
    return authorization