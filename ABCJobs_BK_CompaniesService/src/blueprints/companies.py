from flask import Flask, jsonify, request, Blueprint
from ..commands.create_company import CreateCompany
from ..commands.get_company import GetCompany
from ..commands.get_companies import GetCompanies
from ..commands.authenticate import Authenticate
from ..commands.reset import Reset

import requests
import os

companies_blueprint = Blueprint('companies', __name__)

@companies_blueprint.route('/companies', methods = ['POST'])
def create():
    auth_info = Authenticate(auth_token()).execute()
    company = CreateCompany(data= request.get_json(), userid = auth_info['id'], token = auth_token()).execute()
    return jsonify(company), 201

@companies_blueprint.route('/companies', methods = ['GET'])
def index():
    auth_info = Authenticate(auth_token()).execute()
    companies = GetCompanies(request.args.to_dict(), auth_info['id']).execute()
    return jsonify(companies)

@companies_blueprint.route('/companies/<id>', methods = ['GET'])
def show(id):
    Authenticate(auth_token()).execute()
    company = GetCompany(id).execute()
    return jsonify(company)

@companies_blueprint.route('/companies/ping', methods = ['GET'])
def ping():
    return 'pong'

@companies_blueprint.route('/companies/reset', methods = ['POST'])
def reset():
    Reset().execute()
    return jsonify({'status': 'OK'})

def auth_token():
    if 'Authorization' in request.headers:
        authorization = request.headers['Authorization']
    else:
        authorization = None
    return authorization