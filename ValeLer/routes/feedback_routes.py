from flask import Blueprint
from routes.auth import admin_required
from controllers import feedback_controller

feedback = Blueprint('Feedback', __name__)


@feedback.route('/feedback', methods=['GET', 'POST'])
def feedback_page():
    return feedback_controller.feedback_page()


@feedback.route('/admin/feedbacks')
@admin_required
def feedback_admin_page():
    return feedback_controller.feedback_admin_page()


@feedback.route('/del_feed/<int:id>', methods=['POST'])
@admin_required
def del_feed(id):
    return feedback_controller.del_feed(id)
