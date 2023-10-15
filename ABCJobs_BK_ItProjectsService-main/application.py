from flask import Flask, jsonify
from src.session import Session, engine
from src.models.model import Base
from src.blueprints.projects import projects_blueprint
from src.errors.errors import ApiError

application = Flask(__name__)
application.register_blueprint(projects_blueprint)

Base.metadata.create_all(engine)

@application.errorhandler(ApiError)
def handle_exception(err):
    response = {
      "mssg": err.description 
    }
    return jsonify(response), err.code
  
if __name__ == "__main__":
    application.run( debug = True, port = 5000, host='0.0.0.0')