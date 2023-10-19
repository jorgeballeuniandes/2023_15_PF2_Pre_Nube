from flask import Flask, jsonify, request, Blueprint
from ..commands.create_it_specialist_document import CreateItSpecialistDocument
from ..commands.get_it_specialist_document import GetItSpecialistDocument
from ..commands.get_it_specialist_documents import GetItSpecialistDocuments
from ..commands.get_it_specialist_documents_by_it_specialist_id import GetItSpecialistDocumentsByItSpecialistId
from ..commands.public_create_it_specialist_document import PublicCreateItSpecialistDocument
from ..commands.upload_it_specialist_document import UploadItSpecialistDocument
from ..commands.authenticate import Authenticate
from ..commands.reset import Reset

it_specialist_documents_blueprint = Blueprint('it_specialist_documents', __name__)

@it_specialist_documents_blueprint.route('/it_specialist_documents', methods = ['POST'])
def create():
    auth_info = Authenticate(auth_token()).execute()
    it_specialist_document = CreateItSpecialistDocument(request.get_json(), auth_info['id']).execute()
    return jsonify(it_specialist_document), 201

@it_specialist_documents_blueprint.route('/public/it_specialist_documents', methods = ['POST'])
def public_create():
    auth_info = Authenticate(auth_token()).execute()
    it_specialist_document = PublicCreateItSpecialistDocument(request.get_json(), auth_info['id']).execute()
    return jsonify(it_specialist_document), 201

@it_specialist_documents_blueprint.route('/upload_document', methods = ['POST'])
def upload():
    Authenticate(auth_token()).execute()
    response = UploadItSpecialistDocument().execute()
    return jsonify(response), 201

@it_specialist_documents_blueprint.route('/it_specialist_documents', methods = ['GET'])
def index():
    auth_info = Authenticate(auth_token()).execute()
    it_specialist_documents = GetItSpecialistDocuments(request.args.to_dict(), auth_info['id']).execute()
    return jsonify(it_specialist_documents)

@it_specialist_documents_blueprint.route('/it_specialist_documents/<id>', methods = ['GET'])
def show(id):
    Authenticate(auth_token()).execute()
    it_specialist_document = GetItSpecialistDocument(id).execute()
    return jsonify(it_specialist_document)

@it_specialist_documents_blueprint.route('/it_specialist_documents/byItSpecialistId/<itSpecialistId>', methods = ['GET'])
def show_by_user_id(itSpecialistId):
    Authenticate(auth_token()).execute()
    it_specialist_document = GetItSpecialistDocumentsByItSpecialistId(itSpecialistId).execute()
    return jsonify(it_specialist_document)

@it_specialist_documents_blueprint.route('/it_specialist_documents/ping', methods = ['GET'])
def ping():
    return 'pong'

@it_specialist_documents_blueprint.route('/it_specialist_documents/reset', methods = ['POST'])
def reset():
    Reset().execute()
    return jsonify({'status': 'OK'})

def auth_token():
    if 'Authorization' in request.headers:
        authorization = request.headers['Authorization']
    else:
        authorization = None
    return authorization