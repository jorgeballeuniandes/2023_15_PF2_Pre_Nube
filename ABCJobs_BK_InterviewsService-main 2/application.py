from flask import Flask, jsonify
from src.session import Session, engine
from src.models.model import Base
from src.blueprints.interviews import interviews_blueprint
from src.errors.errors import ApiError

application = Flask(__name__)
application.register_blueprint(interviews_blueprint)

Base.metadata.create_all(engine)

@application.errorhandler(ApiError)
def handle_exception(err):
    response = {
      "mssg": err.description 
    }
    return jsonify(response), err.code

if __name__ == "__main__":
    application.run(port = 5000, debug = True)