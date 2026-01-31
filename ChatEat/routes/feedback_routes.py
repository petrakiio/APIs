from flask import Blueprint, render_template, request, session, redirect, url_for,flash
from routes.auth import login_required

feedback_route = Blueprint('feed',__name__)

@feedback_route.route('/feedback')
@login_required
def feedback():
    return render_template('feedback.html')

@feedback_route.route('/enviar-feed', methods=['POST'])
@login_required
def enviar()
    