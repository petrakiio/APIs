from flask import Blueprint,flash,render_template,url_for
from auth import login_required

login_route = Blueprint('Login',__name__)

@login_route.route('/login')
def login():
    return render_template('login.html')

@login_route.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')
