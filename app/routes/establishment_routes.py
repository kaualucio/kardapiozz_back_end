from flask import Blueprint, jsonify, request
from app.decorators.private_route import private_route
establishment = Blueprint('establishment', __name__)


@establishment.route('/info', methods=['GET'])
@private_route()
def get_info(payload):
  return jsonify({ 'info': payload }), 200