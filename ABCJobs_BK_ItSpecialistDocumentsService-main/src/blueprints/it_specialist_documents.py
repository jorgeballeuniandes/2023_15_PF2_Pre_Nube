from flask import Flask, jsonify, request, Blueprint
from ..commands.create_it_specialist_document import CreateItSpecialistDocument
from ..commands.public_create_it_specialist_document import PublicCreateItSpecialistDocument
from ..commands.authenticate import Authenticate
from ..commands.upload_it_specialist_doc import UploadItSpecialistDoc
from ..commands.get_all_docs_in_folder import GetAllDocsInFolder
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

@it_specialist_documents_blueprint.route('/upload_doc', methods = ['POST'])
def upload_doc():
    Authenticate(auth_token()).execute()
    response = UploadItSpecialistDoc().execute()
    return jsonify(response), 201

@it_specialist_documents_blueprint.route('/it_specialist_files', methods = ['GET'])
def get_all_files_in_folder():
    it_specialist_documents_files = GetAllDocsInFolder().execute()
    return jsonify(it_specialist_documents_files)

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