from flask import Blueprint
from routes.auth import login_required
from controllers import feedback_controller

feedback_route = Blueprint('feed',__name__)

@feedback_route.route('/feedback')
@login_required
def feedback():
    return feedback_controller.feedback()

@feedback_route.route('/enviar-feed', methods=['POST'])
@login_required
def enviar():
    return feedback_controller.enviar()
