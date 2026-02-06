from flask import Blueprint, request, jsonify
from models.gatway_class import Gatway,GatwayService

gatway_route = Blueprint('gatway', __name__)

@gatway_route.route('/iniciar_pagamento/<int:id>')
def iniciar_pagamento(id):
    